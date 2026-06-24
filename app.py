from flask import Flask, request, jsonify, send_from_directory
import joblib
import pandas as pd
import os

app = Flask(__name__)

model = joblib.load("KNN_heart.pkl")
scaler = joblib.load("scaler.pkl")
columns = joblib.load("columns.pkl")

@app.route("/")
def home():
    return send_from_directory(os.path.join(app.root_path, "static"), "index.html")

@app.route("/predict", methods=["POST"])
def predict():
    form = request.json

    data = dict.fromkeys(columns, 0)
    data["Age"] = int(form["age"])
    data["RestingBP"] = int(form["bp"])
    data["Cholesterol"] = int(form["chol"])
    data["FastingBS"] = int(form["fasting"])
    data["MaxHR"] = int(form["maxhr"])
    data["Oldpeak"] = float(form["oldpeak"])

    sex = form["sex"].upper()
    chest = form["chest"].upper()
    ecg = form["ecg"]
    angina = form["angina"].upper()
    slope = form["slope"]

    if sex == "M":
        data["Sex_M"] = 1

    if chest == "ATA":
        data["ChestPainType_ATA"] = 1
    elif chest == "NAP":
        data["ChestPainType_NAP"] = 1
    elif chest == "TA":
        data["ChestPainType_TA"] = 1

    if ecg == "Normal":
        data["RestingECG_Normal"] = 1
    elif ecg == "ST":
        data["RestingECG_ST"] = 1

    if angina == "Y":
        data["ExerciseAngina_Y"] = 1

    if slope == "Flat":
        data["ST_Slope_Flat"] = 1
    elif slope == "Up":
        data["ST_Slope_Up"] = 1

    df = pd.DataFrame([data])
    df_scaled = scaler.transform(df)
    prediction = model.predict(df_scaled)

    if prediction[0] == 1:
        result = "Heart Disease Detected"
    else:
        result = "No Heart Disease Detected"

    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)
