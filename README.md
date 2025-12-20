# Final Project — Verdantia

**Smart Gardening Assistant**
EcoCats — KRR / Machine Learning\

---

## Overview

Verdantia is a smart gardening assistant developed as a final project for a Knowledge Representation and Reasoning / Machine Learning course. The system is designed to help users make basic gardening decisions by combining a machine learning model for crop recommendation with a rule-based approach for plant health diagnosis.

---

## Features

* **Crop Recommendation**
  Predicts a suitable crop based on soil nutrients (N, P, K) and environmental conditions such as temperature, humidity, pH, and rainfall.

* **Plant Health Diagnosis**
  Uses a rule-based system to provide basic assessments of plant health based on user-input conditions, soil type, and climate information.

* **Web Interface**
  A simple Flask-based web interface allows users to interact with both features through a single form.

---

## Project Structure

```
smart-gardening/
├── README.md # Project documentation
├── requirements.txt # Python dependencies
├── .git/ # Git version control data
├── .gitignore # Git ignore rules
├── data/ # Dataset files
│ └── crop_recommendation2_cleaned.csv
├── documentation/ # Project documentation (currently empty)
├── models/ # Trained machine learning models
│ └── crop_model.pkl
├── notebook/ # Jupyter notebooks
│ └── dataset.ipynb # Data exploration and preprocessing
├── src/ # Source code (reserved for future use)
├── utils/ # Helper modules
│ └── rules.py # Rule-based diagnosis logic
├── web_app/ # Flask web application
│ ├── app.py # Main application file
│ ├── static/ # Static assets (CSS, icons)
│ │ ├── style.css
│ │ └── info-icon.svg
│ └── templates/ # HTML templates
│ └── index.html
└── venv/ # Python virtual environment
```

---

## Technologies Used

* Python 3.10+
* Flask (web framework)
* scikit-learn (machine learning)
* NumPy / Pandas (data handling)

---

## Prerequisites

* Windows OS
* Python 3.10 or later
* Virtual environment located at `venv/`

---

## Setup Instructions

1. Activate the virtual environment (PowerShell):

   ```powershell
   cd C:\Smart_Gardening
   .\venv\Scripts\Activate
   ```

2. Install required dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

---

## Running the Application

To start the Flask application locally:

```powershell
python web_app\app.py
```

Then open a browser and go to:

```
http://localhost:5000
```

Optional (using Flask CLI):

```powershell
$env:FLASK_APP="web_app/app.py"
$env:FLASK_ENV="development"
flask run
```

---

## Usage

1. Open the web application in the browser.
2. Choose between **Crop Recommendation** or **Plant Health Diagnosis**.
3. Fill in the required soil and environmental parameters.
4. Submit the form to receive the system output.

The recommendation feature loads a pre-trained model from `models/crop_model.pkl`, while the diagnosis feature applies predefined rules from `utils/rules.py`.

---

## Limitations

* The accuracy of crop recommendations depends on the quality of the training data and model.
* The plant health diagnosis is rule-based and does not cover all possible diseases or conditions.
* The system is intended for educational use and should not be treated as expert agricultural advice.

---

## Troubleshooting

* **Model not loaded**: Ensure that `models/crop_model.pkl` exists and is accessible.
* **Import or module errors**: Verify that the virtual environment is activated and dependencies are installed.
* **Flask not running**: Check that the correct Python version is being used.

---

## Conclusion

This project demonstrates the integration of machine learning and rule-based reasoning in a practical application. Verdantia serves as a proof-of-concept system that applies classroom concepts to a real-world-inspired problem in smart agriculture.

---

## License

This project was created strictly for academic purposes as part of a college course requirement.
