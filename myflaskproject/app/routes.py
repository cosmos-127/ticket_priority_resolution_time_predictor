from flask import render_template
from app import app


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    # Implement your model prediction logic here
    return "Prediction result goes here"
