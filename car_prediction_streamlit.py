import streamlit as st
import pandas as pd
import joblib

# Load the trained model and feature list
try:
    model, final_features = joblib.load('models/tuned_gb_model_and_features.pkl')
except FileNotFoundError:
    st.error("❌ Model file not found: tuned_gb_model_and_features.pkl")
    st.stop()

st.title("🚗 Car Price Predictor")

# --- User Inputs ---
year = st.number_input("Year of Manufacture", min_value=1990, max_value=2025, value=2015)
km_driven = st.number_input("Kilometers Driven", min_value=0, max_value=500000, value=30000)
mileage = st.number_input("Mileage (km/l)", min_value=5.0, max_value=40.0, value=18.0)
fuel_type = st.selectbox("Fuel Type", ['Electric', 'CNG', 'LPG', 'Diesel', 'Petrol'])
seats = st.number_input("Number of Seats", min_value=2, max_value=10, value=5)
transmission = st.selectbox("Transmission", ['Manual', 'Automatic'])
body_type = st.selectbox("Body Type", ['SUV', 'Sedan', 'Hatchback', 'MUV', 'Pickup Trucks', 'Hybrids', 'Wagon', 'Minivans', 'Coupe', 'Convertibles'])
city = st.selectbox("City", ['BANGALORE', 'DELHI', 'CHENNAI', 'HYDERABAD', 'JAIPUR', 'KOLKATA'])
num_gears = st.selectbox("Number of Gears", [4, 5, 6, 7, 8])

# --- Encoding (Exactly how you trained) ---
fuel_order = {'Electric': 0, 'CNG': 1, 'LPG': 2, 'Diesel': 3, 'Petrol': 4}
city_order = {'BANGALORE': 0, 'DELHI': 1, 'CHENNAI': 2, 'HYDERABAD': 3, 'JAIPUR': 4, 'KOLKATA': 5}
transmission_map = {'Manual': 0, 'Automatic': 1}

# label encoding for body type (this was done using LabelEncoder in training)
body_type_map = {
    'SUV': 8,
    'Sedan': 7,
    'Hatchback': 3,
    'MUV': 4,
    'Pickup Trucks': 5,
    'Hybrids': 1,
    'Wagon': 9,
    'Minivans': 6,
    'Coupe': 0,
    'Convertibles': 2
}

# Apply encoding
fuel_encoded = fuel_order.get(fuel_type, 0)
city_encoded = city_order.get(city, 0)
trans_encoded = transmission_map.get(transmission, 0)
body_encoded = body_type_map.get(body_type, 0)

# --- Construct Input Data ---
input_data = pd.DataFrame({
    'YEAR_OF_MANUFACTURE': [year],
    'KILOMETERS_DRIVEN': [km_driven],
    'MILEAGE': [mileage],
    'SEATS': [seats],
    'FUEL_TYPE_ENCODED': [fuel_encoded],
    'TRANSMISSION_ENCODED': [trans_encoded],
    'BODY_TYPE_ENCODED': [body_encoded],
    'CITY_ENCODED': [city_encoded],
    'NUMBER_OF_GEARS': [num_gears]
})

# If any columns are missing that model expects, add them with 0
features_for_prediction = [f for f in final_features if f != 'PRICE']
for feature in features_for_prediction:
    if feature not in input_data.columns:
        input_data[feature] = 0

# Match exact order
input_data = input_data[features_for_prediction]

# --- Predict ---
if st.button("Predict Price"):
    try:
        prediction = model.predict(input_data)
        st.success(f"💰 Estimated Car Price: ₹ {prediction[0]:,.2f}")
    except Exception as e:
        st.error(f"❌ Prediction error: {e}")

#---------------------------------------------------->
# import streamlit as st
# import joblib
# import pandas as pd
# import os

# print("Files in current directory:", os.listdir('.'))
# print("Current working directory:", os.getcwd())

# # Load the trained model and features
# try:
#     model, final_features = joblib.load('tuned_gb_model_and_features.pkl')
#     print("✅ Model and features loaded successfully!")
# except FileNotFoundError:
#     st.error("Error: tuned_gb_model_and_features.pkl not found.")
#     st.stop()

# st.title("Car Price Predictor")

# # Input fields
# year = st.number_input("Year of Manufacture", min_value=1990, max_value=2025, value=2015)
# km_driven = st.number_input("Kilometers Driven", min_value=0, max_value=500000, value=30000)
# mileage = st.number_input("Mileage (km/l)", min_value=5.0, max_value=40.0, value=18.0)
# fuel_type = st.selectbox("Fuel Type", ['Petrol', 'Diesel', 'CNG', 'Electric'])
# seats = st.number_input("Number of Seats", min_value=2, max_value=10, value=5)
# transmission = st.selectbox("Transmission", ['Manual', 'Automatic'])

# # Encoding
# fuel_map = {'Petrol': 0, 'Diesel': 1, 'CNG': 2, 'Electric': 3}
# fuel_encoded = fuel_map[fuel_type]
# transmission_encoded = {'Manual': 1, 'Automatic': 0}[transmission]

# # Derived features
# car_age = 2023 - year
# annual_km = km_driven / (car_age + 1)

# # --- CRITICAL: Create input_data with ALL features ---
# features_for_prediction = [f for f in final_features if f != 'PRICE']  # Exclude 'PRICE'

# input_data = pd.DataFrame({
#     'KILOMETERS_DRIVEN': [km_driven],
#     'YEAR_OF_MANUFACTURE': [year],
#     'MILEAGE': [mileage],
#     'car_age': [car_age],
#     'annual_km': [annual_km],
#     'Seats': [seats],
#     'FUEL_TYPE_Diesel': [1 if fuel_type == 'Diesel' else 0],
#     'FUEL_TYPE_Petrol': [1 if fuel_type == 'Petrol' else 0],
#     'TRANSMISSION_Manual': [transmission_encoded],
#     # ... Add ALL other features from final_features (except 'PRICE')
# })

# # Ensure all required columns are present (even if 0 or dummy values)
# for feature in features_for_prediction:
#     if feature not in input_data.columns:
#         input_data[feature] = 0  # Or a more appropriate default value

# input_data = input_data[features_for_prediction]  # Order columns to match training

# if st.button("Predict Price"):
#     try:
#         prediction = model.predict(input_data)
#         st.success(f"💰 Estimated Car Price: ₹ {prediction[0]:,.2f}")
#     except Exception as e:
#         st.error(f"Prediction error: {e}")


#--------------------------------------------------------->2.0
# import streamlit as st
# import joblib
# import pandas as pd

# # Load the model
# gb_model = joblib.load('tuned_gb_model.pkl')

# st.title("🚗 Car Price Predictor")

# # 🔼 Move these inputs before the DataFrame
# year = st.number_input("Year of Manufacture", min_value=1990, max_value=2025, value=2015)
# km_driven = st.number_input("Kilometers Driven", min_value=0, max_value=500000, value=30000)
# mileage = st.number_input("Mileage (km/l)", min_value=5.0, max_value=40.0, value=18.0)
# fuel_type = st.selectbox("Fuel Type", ['Petrol', 'Diesel', 'CNG', 'Electric'])

# # Encoding
# fuel_map = {'Petrol': 0, 'Diesel': 1, 'CNG': 2, 'Electric': 3}
# fuel_encoded = fuel_map[fuel_type]

# # Derived features
# car_age = 2023 - year
# annual_km = km_driven / (car_age + 1)

# # ✅ Now build the DataFrame
# input_data = pd.DataFrame({
#     'KILOMETERS_DRIVEN': [km_driven],
#     'YEAR_OF_MANUFACTURE': [year],
#     'MILEAGE': [mileage],
#     'FUEL_TYPE_ENCODED': [fuel_encoded],
#     'car_age': [car_age],
#     'annual_km': [annual_km],
#     # Add any additional features if required by your model
# })

# if st.button("Predict Price"):
#     prediction = gb_model.predict(input_data)
#     st.success(f"💰 Estimated Car Price: ₹ {prediction[0]:,.2f}")


# import streamlit as st
# import pandas as pd
# import numpy as np
# import joblib


# # Save the trained model
# joblib.dump(final_model, 'final_model.pkl')
# print("✅ Model saved as final_model.pkl")


# # Load trained model
# model = joblib.load('final_model.pkl')  # Your Gradient Boosting or best model

# st.title("🚗 Car Price Predictor")
# st.markdown("Enter car details below to predict the estimated resale price.")

# # Input fields
# year = st.number_input("Year of Manufacture", min_value=1990, max_value=2025, value=2015)
# km_driven = st.number_input("Kilometers Driven", min_value=0, max_value=500000, value=30000)
# mileage = st.number_input("Mileage (km/l)", min_value=5.0, max_value=40.0, value=18.0)
# fuel_type = st.selectbox("Fuel Type", ['Petrol', 'Diesel', 'CNG', 'Electric'])

# # Optional: Encode or preprocess inputs (simplified here)
# fuel_map = {'Petrol': 0, 'Diesel': 1, 'CNG': 2, 'Electric': 3}
# fuel_encoded = fuel_map[fuel_type]

# # Derived features
# car_age = 2023 - year
# annual_km = km_driven / (car_age + 1)

# # Create DataFrame for prediction
# input_data = pd.DataFrame({
#     'KILOMETERS_DRIVEN': [km_driven],
#     'YEAR_OF_MANUFACTURE': [year],
#     'MILEAGE': [mileage],
#     'FUEL_TYPE_ENCODED': [fuel_encoded],
#     'car_age': [car_age],
#     'annual_km': [annual_km],
#     # Add all other required features as per your model's training
# })

# # Prediction
# if st.button("Predict Price"):
#     prediction = model.predict(input_data)
#     st.success(f"💰 Estimated Car Price: ₹ {prediction[0]:,.2f}")
