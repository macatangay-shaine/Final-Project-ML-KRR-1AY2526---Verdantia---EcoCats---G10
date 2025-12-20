# Final-Project-ML-KRR-1AY2526 — Verdantia — EcoCats — G10

Verdantia is a smart gardening assistant that recommends crops based on soil and environmental inputs, and diagnoses plant health using rule-based checks.

## Project Structure

```
smart-gardening/
├── data/          # Data files and datasets
├── models/        # Machine learning models (e.g., crop_model.pkl)
├── utils/         # Rule-based diagnosis helpers
├── web_app/       # Flask web application (UI)
├── requirements.txt
└── README.md
```

## Prerequisites

- Python 3.10+ on Windows
- Virtual environment located at `venv/`

## Setup

1. Activate the virtual environment (PowerShell):
   ```powershell
   cd C:\Smart_Gardening
   .\venv\Scripts\Activate
   ```

2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

## Run (Local)

Run the Flask app and open the browser:

```powershell
python web_app\app.py
# then open http://localhost:5000
```

Optional (Flask runner):

```powershell
$env:FLASK_APP="web_app/app.py"
$env:FLASK_ENV="development"
flask run
```

## Usage

- Recommendation mode: Predicts a suitable crop using `models/crop_model.pkl` based on inputs for N/P/K, temperature, humidity, pH, and rainfall.
- Diagnosis mode: Rule-based assessment using `utils/rules.py` with additional fields like soil type, climate, and current plant.

All interactions are via the form on the home page.

## Troubleshooting

- "Model not loaded" — ensure `models/crop_model.pkl` exists.
- Import errors — confirm the virtual environment is activated and `pip install -r requirements.txt` completed.

## License

Project for academic purposes. Add license information here if needed.
