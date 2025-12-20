from flask import Flask, render_template, request
import joblib
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.rules import apply_rules

app = Flask(__name__)

# Load model using absolute path
model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "crop_model.pkl")
try:
    model = joblib.load(model_path)
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        try:
            mode = request.form.get("mode", "recommend")
            
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

            if mode == "recommend":
                # Crop Recommendation Mode
                if model is None:
                    error = "Model not loaded. Please ensure crop_model.pkl exists in the models folder."
                else:
                    X = pd.DataFrame([[inputs["n"], inputs["p"], inputs["k"],
                                       inputs["temperature"], inputs["humidity"],
                                       inputs["ph"], inputs["rainfall"]]],
                                     columns=["n", "p", "k", "temperature", "humidity", "ph", "rainfall"])

                    crop = model.predict(X)[0]
                    
                    result = {
                        "mode": "recommend",
                        "crop": crop,
                        "message": f"Based on your soil and environmental conditions, we recommend planting {crop}.",
                        "inputs": inputs
                    }
            
            elif mode == "diagnose":
                # Plant Health Diagnosis Mode
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

    return render_template("index.html", result=result, error=error)

if __name__ == "__main__":
    app.run(debug=True)
