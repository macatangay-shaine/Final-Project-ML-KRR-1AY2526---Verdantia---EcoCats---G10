from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.utils import secure_filename
import joblib
import pandas as pd
import sys
import os

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

    return render_template(
        "profile.html",
        profile_username=session.get("profile_username"),
        profile_avatar=session.get("profile_avatar"),
        profile_age=session.get("profile_age"),
        profile_favorite=session.get("profile_favorite"),
        profile_bio=session.get("profile_bio"),
    )

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

            if model is None:
                error = "Model not loaded. Please ensure crop_model.pkl exists in the models folder."
            else:
                X = pd.DataFrame([[inputs["n"], inputs["p"], inputs["k"], inputs["temperature"], inputs["humidity"], inputs["ph"], inputs["rainfall"]]],
                                 columns=["n", "p", "k", "temperature", "humidity", "ph", "rainfall"])
                crop = model.predict(X)[0]
                result = {
                    "mode": "recommend",
                    "crop": crop,
                    "message": f"Based on your soil and environmental conditions, we recommend planting {crop}.",
                    "inputs": inputs
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
