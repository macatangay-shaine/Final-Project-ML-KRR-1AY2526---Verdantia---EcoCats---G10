from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.utils import secure_filename
import joblib
import pandas as pd
import sys
import os
import math
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.rules import apply_rules

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key")

# Uploads
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Load model using absolute path
model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "crop_model.pkl")
try:
    model = joblib.load(model_path)
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Load dataset for fallback multi-crop suggestions
data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "crop_recommendation2_cleaned.csv")
df = None
try:
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
except Exception as e:
    print(f"Error loading dataset: {e}")
    df = None

def top_crops_by_dataset(inputs, k=5):
    """Return top-k crop names ranked by similarity to inputs using the dataset.
    Uses min-max normalization on available numeric features and groups by crop label.
    """
    if df is None:
        return []

    # Detect label column
    label_col = None
    for c in df.columns:
        lc = str(c).strip().lower()
        if lc in ("label", "crop", "crops"):
            label_col = c
            break
    if not label_col:
        return []

    feature_cols = [c for c in ["n","p","k","temperature","humidity","ph","rainfall"] if c in df.columns]
    if not feature_cols:
        return []

    work = df[[label_col] + feature_cols].copy()
    # Min-max scale
    mins = work[feature_cols].min()
    maxs = work[feature_cols].max()
    ranges = (maxs - mins).replace(0, 1)

    # Build input vector
    try:
        x = pd.Series({c: float(inputs[c]) for c in feature_cols})
    except Exception:
        return []

    x_norm = (x - mins) / ranges
    X_norm = (work[feature_cols] - mins) / ranges
    # Compute distances
    dists = ((X_norm - x_norm) ** 2).sum(axis=1) ** 0.5
    work["_dist"] = dists

    # Best distance per crop
    best = work.groupby(label_col)["_dist"].min().reset_index().sort_values("_dist")
    if best.empty:
        return []

    # Convert to suitability score (higher is better)
    d_max = best["_dist"].max()
    eps = 1e-9
    best["suitability"] = ((1.0 - best["_dist"] / (d_max + eps)) * 100).clip(lower=0, upper=100)

    suggestions = []
    for _, row in best.head(max(1, int(k))).iterrows():
        suggestions.append({
            "crop": str(row[label_col]).strip(),
            "suitability": int(round(row["suitability"]))
        })
    return suggestions

# Load dataset for fallback multi-crop suggestions
dataset_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "crop_recommendation2_cleaned.csv")
dataset_df = None
if os.path.exists(dataset_path):
    try:
        dataset_df = pd.read_csv(dataset_path)
    except Exception as e:
        print(f"Error loading dataset fallback: {e}")
        dataset_df = None

TOP_N = int(os.environ.get("VERDANTIA_TOP_N", "5"))

def top_candidates_from_model(X: pd.DataFrame, top_n: int):
    """Return top-N crops using model probabilities, if available."""
    try:
        if not hasattr(model, "predict_proba"):
            return None
        proba = model.predict_proba(X)[0]
        classes = getattr(model, "classes_", None)
        if classes is None:
            return None
        pairs = list(zip(classes, proba))
        pairs.sort(key=lambda p: p[1], reverse=True)
        return [{"crop": c, "confidence": round(p * 100, 1)} for c, p in pairs[:max(1, top_n)]]
    except Exception:
        return None

def top_candidates_from_dataset(inputs: dict, top_n: int, nearest_k: int = 200):
    """Fallback: find nearest samples in dataset and return top-N labels."""
    if dataset_df is None:
        return None
    try:
        feats = ["n", "p", "k", "temperature", "humidity", "ph", "rainfall"]
        q = np.array([float(inputs[f]) for f in feats], dtype=float)
        M = dataset_df[feats].to_numpy(dtype=float)
        # Euclidean distance
        dists = np.linalg.norm(M - q, axis=1)
        idx = np.argsort(dists)[:nearest_k]
        nearest = dataset_df.iloc[idx]
        # Score by average inverse distance and frequency
        nearest = nearest.assign(_dist=dists[idx])
        # Avoid division by zero
        nearest["_inv"] = nearest["_dist"].apply(lambda x: 1.0 / (x + 1e-6))
        agg = nearest.groupby("label").agg(freq=("label", "count"), inv=("_inv", "mean")).reset_index()
        # Composite score: frequency * inverse distance
        agg["score"] = agg["freq"] * agg["inv"]
        agg.sort_values("score", ascending=False, inplace=True)
        total_freq = float(agg["freq"].sum()) or 1.0
        out = []
        for _, row in agg.head(max(1, top_n)).iterrows():
            out.append({
                "crop": row["label"],
                "confidence": round(100.0 * (row["freq"] / total_freq), 1)
            })
        return out
    except Exception:
        return None

@app.route("/")
def landing():
    return render_template(
        "landing.html",
        profile_username=session.get("profile_username"),
        profile_avatar=session.get("profile_avatar"),
    )

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "POST":
        # Save basic profile info in session
        session["profile_username"] = (request.form.get("username", "").strip() or None)
        session["profile_age"] = (request.form.get("age", "").strip() or None)
        session["profile_favorite"] = (request.form.get("favorite", "").strip() or None)
        session["profile_bio"] = (request.form.get("bio", "").strip() or None)

        # Optional avatar upload
        avatar = request.files.get("avatar")
        if avatar and avatar.filename:
            fname = secure_filename(avatar.filename)
            save_path = os.path.join(app.config["UPLOAD_FOLDER"], fname)
            try:
                avatar.save(save_path)
                session["profile_avatar"] = fname
            except Exception:
                # If saving fails, just skip storing an avatar
                pass

        return redirect(url_for("mode_select"))
    # The dedicated profile page was removed; redirect to mode selection.
    return redirect(url_for("mode_select"))

@app.route("/select")
def mode_select():
    return render_template(
        "mode_select.html",
        profile_username=session.get("profile_username"),
        profile_avatar=session.get("profile_avatar"),
    )

@app.route("/recommend", methods=["GET", "POST"])
def recommend():
    result = None
    error = None
    if request.method == "POST":
        try:
            profile_username = request.form.get("profile_username")
            profile_avatar = request.form.get("profile_avatar")
            if profile_username is not None:
                session["profile_username"] = profile_username.strip()
            if profile_avatar is not None:
                session["profile_avatar"] = profile_avatar

            inputs = {
                "n": float(request.form["n"]),
                "p": float(request.form["p"]),
                "k": float(request.form["k"]),
                "temperature": float(request.form["temperature"]),
                "humidity": float(request.form["humidity"]),
                "ph": float(request.form["ph"]),
                "rainfall": float(request.form["rainfall"]),
                "soil_type": request.form["soil_type"],
                "climate": request.form["climate"]
            }

            X = pd.DataFrame([[inputs["n"], inputs["p"], inputs["k"], inputs["temperature"], inputs["humidity"], inputs["ph"], inputs["rainfall"]]],
                             columns=["n", "p", "k", "temperature", "humidity", "ph", "rainfall"])

            candidates = None
            primary_crop = None
            # Try model top-N first
            suggestions = []
            primary_crop = None

            if model is not None:
                X = pd.DataFrame([[inputs["n"], inputs["p"], inputs["k"], inputs["temperature"], inputs["humidity"], inputs["ph"], inputs["rainfall"]]],
                                 columns=["n", "p", "k", "temperature", "humidity", "ph", "rainfall"])
                try:
                    # Prefer probability-based ranking when available
                    if hasattr(model, "predict_proba"):
                        proba = model.predict_proba(X)[0]
                        classes = list(getattr(model, "classes_", []))
                        ranked = sorted(zip(classes, proba), key=lambda t: t[1], reverse=True)
                        for crop_name, p in ranked[:5]:
                            suggestions.append({"crop": str(crop_name), "suitability": int(round(p * 100))})
                        if suggestions:
                            primary_crop = suggestions[0]["crop"]
                    else:
                        # Fallback: single prediction plus dataset-based ranking
                        primary_crop = str(model.predict(X)[0])
                except Exception:
                    # Model exists but failed; ignore and use dataset fallback
                    pass

            # Dataset-based ranking if needed or to supplement
            if not suggestions:
                suggestions = top_crops_by_dataset(inputs, k=5)
                if suggestions:
                    primary_crop = suggestions[0]["crop"]

            if primary_crop is None and not suggestions:
                error = "Unable to generate recommendations at this time."
            else:
                if primary_crop is None and suggestions:
                    primary_crop = suggestions[0]["crop"]
                # Build result structure; keep top as primary and provide several alternatives
                result = {
                    "mode": "recommend",
                    "crop": primary_crop,
                    "message": "Top matches ranked by suitability to your conditions.",
                    "inputs": inputs,
                    "alternatives": [s for s in suggestions if s.get("crop") != primary_crop]
                }
        except Exception as e:
            error = f"Error processing request: {str(e)}"

    return render_template("recommend.html", result=result, error=error)

@app.route("/advisor", methods=["GET", "POST"])
def advisor():
    result = None
    error = None
    if request.method == "POST":
        try:
            profile_username = request.form.get("profile_username")
            profile_avatar = request.form.get("profile_avatar")
            if profile_username is not None:
                session["profile_username"] = profile_username.strip()
            if profile_avatar is not None:
                session["profile_avatar"] = profile_avatar

            inputs = {
                "n": float(request.form["n"]),
                "p": float(request.form["p"]),
                "k": float(request.form["k"]),
                "temperature": float(request.form["temperature"]),
                "humidity": float(request.form["humidity"]),
                "ph": float(request.form["ph"]),
                "rainfall": float(request.form["rainfall"]),
                "soil_type": request.form["soil_type"],
                "climate": request.form["climate"]
            }
            current_plant = request.form.get("current_plant", "your plant")
            inputs["crop"] = current_plant
            condition, reason, advice = apply_rules(inputs)
            result = {
                "mode": "diagnose",
                "plant": current_plant,
                "condition": condition,
                "reason": reason,
                "advice": advice,
                "inputs": inputs
            }
        except Exception as e:
            error = f"Error processing request: {str(e)}"

    return render_template("advisor.html", result=result, error=error)

# Static files are served from /static by default (web_app/static)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))

if __name__ == "__main__":
    app.run(debug=True)
