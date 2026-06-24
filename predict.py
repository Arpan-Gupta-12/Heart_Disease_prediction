import joblib
import pandas as pd


model = joblib.load("KNN_heart.pkl")
scaler = joblib.load("scaler.pkl")
columns=joblib.load("columns.pkl")


age = int(input("Age: "))
bp = int(input("Resting BP: "))
chol = int(input("Cholesterol: "))
fasting = int(input("FastingBS (0/1): "))
maxhr = int(input("MaxHR: "))
oldpeak = float(input("Oldpeak: "))
sex = input("Sex (M/F): ").upper()
chest = input("ChestPainType (ATA/NAP/TA/ASY): ").upper()
ecg = input("RestingECG (Normal/ST/LVH): ")
angina = input("ExerciseAngina (Y/N): ").upper()
slope = input("ST_Slope (Up/Flat/Down): ")

data = dict.fromkeys(columns, 0)
data["Age"] = age
data["RestingBP"] = bp
data["Cholesterol"] = chol
data["FastingBS"] = fasting
data["MaxHR"] = maxhr
data["Oldpeak"] = oldpeak

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
    print("\n Heart Disease Detected")
else:
    print("\n No Heart Disease Detected")