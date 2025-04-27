import streamlit as st
import pandas as pd
import joblib
import json
import numpy as np
from sklearn.preprocessing import OrdinalEncoder, LabelEncoder

# Page Configuration
st.set_page_config(page_title="Car Price Predictor", page_icon="🚗", layout="wide")

# Custom CSS
st.markdown("""
<style>
.prediction-card {
    border: 2px solid #4CAF50;
    padding: 20px;
    border-radius: 10px;
    margin-top: 20px;
    background-color: #f9f9f9;
}
.prediction-card h3 {
    color: #4CAF50;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# Hardcoded category orders as fallback
DEFAULT_ORDERS = {
    'insurance_order': ['Not Available', '1', '2', 'Third Party', 'Third Party insurance', 'Comprehensive', 'Zero Dep'],
    'city_order': ['BANGALORE', 'DELHI', 'CHENNAI', 'HYDERABAD', 'JAIPUR', 'KOLKATA'],
    'fuel_order': ['Electric', 'CNG', 'LPG', 'Diesel', 'Petrol'],
    'car_ranking': ['SUV', 'Sedan', 'Hatchback', 'MUV', 'Pickup Trucks', 'Hybrids', 'Wagon', 'Minivans', 'Coupe', 'Convertibles']
}

@st.cache_resource
def load_assets():
    try:
        # Load model
        model = joblib.load('tuned_gb_model.pkl')

        # Load metadata with fallback
        try:
            with open('model_metadata.json') as f:
                metadata = json.load(f)
            metadata = {**DEFAULT_ORDERS, **metadata}
        except (FileNotFoundError, json.JSONDecodeError):
            metadata = DEFAULT_ORDERS
            st.warning("Using default category orders")

        encoders = {}

        for enc_name in ['insurance', 'city', 'fuel', 'body_type']:
            try:
                encoders[enc_name] = joblib.load(f'{enc_name}_encoder.pkl')
                st.success(f"Loaded pre-fitted {enc_name} encoder")
            except:
                st.warning(f"Couldn't load {enc_name} encoder — creating new one")
                if enc_name in ['insurance', 'city', 'fuel']:
                    encoders[enc_name] = OrdinalEncoder(categories=[metadata[f'{enc_name}_order']],
                                                        handle_unknown='use_encoded_value', unknown_value=-1)
                    encoders[enc_name].fit([[x] for x in metadata[f'{enc_name}_order']])
                elif enc_name == 'body_type':
                    encoders[enc_name] = LabelEncoder()
                    encoders[enc_name].fit(metadata['car_ranking'])

        return model, metadata, encoders

    except Exception as e:
        st.error(f"Error loading assets: {str(e)}")
        st.stop()


def preprocess_input(input_df, encoders, metadata):
    """Preprocess input data with guaranteed fitted encoders"""
    try:
        # Create a copy to avoid modifying original
        processed = input_df.copy()

        # Apply encodings
        processed['INSURANCE_ENCODED'] = encoders['insurance'].transform(processed[['INSURANCE_VALIDITY']])
        processed['CITY_ENCODED'] = encoders['city'].transform(processed[['CITY_NAME']])
        processed['FUEL_TYPE_ENCODED'] = encoders['fuel'].transform(processed[['FUEL_TYPE']])

        # One-hot encoding for fuel types
        processed['FUEL_TYPE_Diesel'] = (processed['FUEL_TYPE'] == 'Diesel').astype(int)
        processed['FUEL_TYPE_Petrol'] = (processed['FUEL_TYPE'] == 'Petrol').astype(int)

        # Body type encoding
        processed['BODY_TYPE_ENCODED'] = encoders['body_type'].transform(processed[['BODY_TYPE']]) # Pass as DataFrame

        # Transmission encoding
        processed['TRANSMISSION_ENCODED'] = processed['TRANSMISSION'].map({'Manual':0, 'Automatic':1})

        return processed.drop(columns=['FUEL_TYPE', 'CITY_NAME', 'INSURANCE_VALIDITY', 'BODY_TYPE'])

    except Exception as e:
        st.error(f"Preprocessing error: {str(e)}")
        st.stop()

def main():
    st.title("🚗 Car Price Prediction")

    # Load assets (guaranteed to have fitted encoders)
    model, metadata, encoders = load_assets()

    # Input Section
    with st.form("car_details"):
        col1, col2 = st.columns(2)
        with col1:
            year = st.number_input("Manufacture Year", min_value=1990, max_value=2025, value=2015)
            km_driven = st.number_input("Kilometers Driven", min_value=0, max_value=500000, value=50000)
            mileage = st.number_input("Mileage (kmpl)", min_value=5.0, max_value=40.0, value=15.0)
        with col2:
            seats = st.number_input("Seats", min_value=2, max_value=10, value=5)
            fuel_type = st.selectbox("Fuel Type", metadata['fuel_order'])
            transmission = st.selectbox("Transmission", ['Manual', 'Automatic'])
            body_type = st.selectbox("Body Type", metadata['car_ranking'])
            city = st.selectbox("City", metadata['city_order'])
            insurance = st.selectbox("Insurance", metadata['insurance_order'])

        if st.form_submit_button("Estimate Price", type="primary"):
            with st.spinner("Calculating..."):
                try:
                    # Prepare and preprocess input
                    input_data = pd.DataFrame({
                        'YEAR_OF_MANUFACTURE': [year],
                        'KILOMETERS_DRIVEN': [km_driven],
                        'MILEAGE': [mileage],
                        'Seats': [seats],
                        'FUEL_TYPE': [fuel_type],
                        'TRANSMISSION': [transmission],
                        'BODY_TYPE': [body_type],
                        'CITY_NAME': [city],
                        'INSURANCE_VALIDITY': [insurance]
                    })

                    processed = preprocess_input(input_data, encoders, metadata)
                    price = model.predict(processed)[0]

                    # Display result
                    st.markdown(f"""
                    <div class="prediction-card">
                        <h3>Estimated Market Value: ₹{price:,.2f}</h3>
                    </div>
                    """, unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Prediction failed: {str(e)}")

if __name__ == "__main__":
    main()
#------>
# import streamlit as st
# import pandas as pd
# import joblib
# import json
# from sklearn.preprocessing import OrdinalEncoder, LabelEncoder

# # Page Configuration
# st.set_page_config(
#     page_title="Car Price Predictor",
#     page_icon="🚗",
#     layout="wide"
# )

# # Custom CSS
# st.markdown("""
# <style>
#     .prediction-card {
#         background-color: #e8f5e9;
#         padding: 20px;
#         border-radius: 10px;
#         margin-top: 20px;
#         border-left: 5px solid #4CAF50;
#     }
#     .stButton>button {
#         background-color: #4CAF50;
#         color: white;
#     }
#     .input-section {
#         background-color: #f5f5f5;
#         padding: 20px;
#         border-radius: 10px;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Hardcoded category orders as fallback
# DEFAULT_ORDERS = {
#     'insurance_order': [
#         'Not Available',
#         '1', 
#         '2',
#         'Third Party', 
#         'Third Party insurance',
#         'Comprehensive',
#         'Zero Dep'
#     ],
#     'city_order': ['BANGALORE', 'DELHI', 'CHENNAI', 'HYDERABAD', 'JAIPUR', 'KOLKATA'],
#     'fuel_order': ['Electric', 'CNG', 'LPG', 'Diesel', 'Petrol'],
#     'car_ranking': ['SUV', 'Sedan', 'Hatchback', 'MUV', 'Pickup Trucks', 'Hybrids', 
#                    'Wagon', 'Minivans', 'Coupe', 'Convertibles']
# }

# @st.cache_resource
# def load_assets():
#     try:
#         # Load model
#         model = joblib.load('tuned_gb_model.pkl')
        
#         # Load metadata with fallback
#         try:
#             with open('model_metadata.json') as f:
#                 metadata = json.load(f)
#             # Merge with defaults for any missing keys
#             metadata = {**DEFAULT_ORDERS, **metadata}
#         except:
#             metadata = DEFAULT_ORDERS
#             st.warning("Using default category orders - ensure they match your training data")
        
#         # Create encoders with proper categories
#         encoders = {
#             'insurance': OrdinalEncoder(categories=[metadata['insurance_order']]),
#             'city': OrdinalEncoder(categories=[metadata['city_order']]),
#             'fuel': OrdinalEncoder(categories=[metadata['fuel_order']]),
#             'body_type': LabelEncoder()
#         }
        
#         # Try to load pre-fitted encoders if available
#         for enc_name in encoders:
#             try:
#                 encoders[enc_name] = joblib.load(f'{enc_name}_encoder.pkl')
#             except:
#                 st.warning(f"Couldn't load fitted {enc_name} encoder - using new instance")
        
#         return model, metadata, encoders
        
#     except Exception as e:
#         st.error(f"Error loading assets: {str(e)}")
#         st.stop()

# def preprocess_input(input_df, encoders, metadata):
#     """Handle all preprocessing steps with error checking"""
#     try:
#         # Apply encodings with error handling
#         if 'INSURANCE_VALIDITY' in input_df.columns:
#             input_df['INSURANCE_ENCODED'] = encoders['insurance'].transform(
#                 input_df[['INSURANCE_VALIDITY']])
        
#         if 'CITY_NAME' in input_df.columns:
#             input_df['CITY_ENCODED'] = encoders['city'].transform(
#                 input_df[['CITY_NAME']])
        
#         if 'FUEL_TYPE' in input_df.columns:
#             input_df['FUEL_TYPE_ENCODED'] = encoders['fuel'].transform(
#                 input_df[['FUEL_TYPE']])
            
#             # One-hot encoding for specific fuel types
#             for fuel in ['Diesel', 'Petrol']:
#                 input_df[f'FUEL_TYPE_{fuel}'] = (input_df['FUEL_TYPE'] == fuel).astype(int)
        
#         if 'BODY_TYPE' in input_df.columns:
#             try:
#                 input_df['BODY_TYPE_ENCODED'] = encoders['body_type'].transform(
#                     input_df[['BODY_TYPE']])
#             except:
#                 # Fallback manual encoding
#                 body_mapping = {k:i for i,k in enumerate(metadata['car_ranking'])}
#                 input_df['BODY_TYPE_ENCODED'] = input_df['BODY_TYPE'].map(body_mapping)
        
#         if 'TRANSMISSION' in input_df.columns:
#             input_df['TRANSMISSION_ENCODED'] = input_df['TRANSMISSION'].map(
#                 {'Manual': 0, 'Automatic': 1})
        
#         return input_df
        
#     except Exception as e:
#         st.error(f"Preprocessing error: {str(e)}")
#         st.stop()

# def main():
#     st.title("🚗 Car Price Prediction")
    
#     # Load assets
#     model, metadata, encoders = load_assets()
    
#     # Input Section
#     with st.container():
#         st.header("Enter Vehicle Details")
#         col1, col2 = st.columns(2)
        
#         with col1:
#             year = st.number_input("Manufacture Year", 
#                                  min_value=1990, max_value=2025, value=2015)
#             km_driven = st.number_input("Kilometers Driven", 
#                                       min_value=0, max_value=500000, value=50000)
#             mileage = st.number_input("Mileage (kmpl)", 
#                                     min_value=5.0, max_value=40.0, value=15.0)
            
#         with col2:
#             seats = st.number_input("Seats", min_value=2, max_value=10, value=5)
#             fuel_type = st.selectbox("Fuel Type", metadata['fuel_order'])
#             transmission = st.selectbox("Transmission", ['Manual', 'Automatic'])
#             body_type = st.selectbox("Body Type", metadata['car_ranking'])
#             city = st.selectbox("City", metadata['city_order'])
#             insurance = st.selectbox("Insurance", 
#                                    list(metadata.get('insurance_mapping', {}).values()) or 
#                                    metadata['insurance_order'])
    
#     if st.button("Estimate Price", type="primary"):
#         with st.spinner("Calculating..."):
#             try:
#                 # Prepare input data
#                 input_data = pd.DataFrame({
#                     'YEAR_OF_MANUFACTURE': [year],
#                     'KILOMETERS_DRIVEN': [km_driven],
#                     'MILEAGE': [mileage],
#                     'Seats': [seats],
#                     'FUEL_TYPE': [fuel_type],
#                     'TRANSMISSION': [transmission],
#                     'BODY_TYPE': [body_type],
#                     'CITY_NAME': [city],
#                     'INSURANCE_VALIDITY': [insurance]
#                 })
                
#                 # Preprocess
#                 processed_data = preprocess_input(input_data, encoders, metadata)
                
#                 # Predict
#                 price = model.predict(processed_data)[0]
                
#                 # Display result
#                 st.markdown(f"""
#                 <div class="prediction-card">
#                     <h3>Estimated Market Value: ₹{price:,.2f}</h3>
#                 </div>
#                 """, unsafe_allow_html=True)
                
#             except Exception as e:
#                 st.error(f"Prediction failed: {str(e)}")

# if __name__ == "__main__":
#     main()

# import streamlit as st
# import pandas as pd
# import joblib
# import json
# import numpy as np
# from sklearn.preprocessing import OrdinalEncoder, LabelEncoder

# # Page Configuration
# st.set_page_config(
#     page_title="Car Price Predictor",
#     page_icon="🚗",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Custom CSS for better styling
# st.markdown("""
# <style>
#     .stNumberInput, .stSelectbox {margin-bottom: 1rem;}
#     .stButton>button {background-color: #4CAF50; color: white;}
#     .stAlert {border-radius: 10px;}
#     .prediction-result {font-size: 24px; font-weight: bold; color: #2E8B57;}
# </style>
# """, unsafe_allow_html=True)

# # Load Assets Function
# @st.cache_resource
# def load_assets():
#     """Load all required models and metadata"""
#     try:
#         # Load the full pipeline
#         pipeline = joblib.load('full_pipeline.pkl')
        
#         # Load metadata
#         with open('model_metadata.json', 'r') as f:
#             metadata = json.load(f)
            
#         # Load feature columns
#         feature_columns = joblib.load('feature_columns.pkl')
        
#         return pipeline, metadata, feature_columns
        
#     except Exception as e:
#         st.error(f"❌ Error loading model assets: {str(e)}")
#         st.stop()

# # Main App
# def main():
#     st.title("🚗 Car Price Prediction Dashboard")
#     st.markdown("Predict the market value of your car based on its specifications")
    
#     # Load models and metadata
#     pipeline, metadata, feature_columns = load_assets()
    
#     with st.form("car_details_form"):
#         st.header("Vehicle Specifications")
        
#         col1, col2, col3 = st.columns(3)
        
#         with col1:
#             year = st.number_input("Year of Manufacture", 
#                                  min_value=1990, max_value=2025, value=2015)
#             km_driven = st.number_input("Kilometers Driven", 
#                                       min_value=0, max_value=500000, value=30000)
#             mileage = st.number_input("Mileage (km/l)", 
#                                     min_value=5.0, max_value=40.0, value=18.0)
            
#         with col2:
#             fuel_type = st.selectbox("Fuel Type", metadata['fuel_order'])
#             seats = st.number_input("Number of Seats", 
#                                   min_value=2, max_value=10, value=5)
#             transmission = st.selectbox("Transmission", ['Manual', 'Automatic'])
            
#         with col3:
#             body_type = st.selectbox("Body Type", metadata['car_ranking'])
#             city = st.selectbox("City", metadata['city_order'])
#             insurance = st.selectbox("Insurance Validity", 
#                                    list(metadata['insurance_mapping'].values()))
            
#         submitted = st.form_submit_button("Predict Price", type="primary")
    
#     if submitted:
#         try:
#             # Reverse insurance mapping to get encoded value
#             reverse_insurance_map = {v:k for k,v in metadata['insurance_mapping'].items()}
#             insurance_encoded = reverse_insurance_map[insurance]
            
#             # Create input DataFrame with raw values
#             input_data = pd.DataFrame({
#                 'YEAR_OF_MANUFACTURE': [year],
#                 'KILOMETERS_DRIVEN': [km_driven],
#                 'MILEAGE': [mileage],
#                 'Seats': [seats],
#                 'FUEL_TYPE': [fuel_type],
#                 'TRANSMISSION': [transmission],
#                 'BODY_TYPE': [body_type],
#                 'CITY_NAME': [city],
#                 'INSURANCE_VALIDITY': [insurance_encoded]  # Using encoded value
#             })
            
#             # Preprocess the input data using the pipeline
#             # The pipeline will handle all the encoding automatically
#             prediction = pipeline.predict(input_data)
            
#             # Format the prediction nicely
#             formatted_price = f"₹{prediction[0]:,.2f}"
            
#             # Display results
#             st.success("### Prediction Result")
#             st.markdown(f"""
#             <div class="prediction-result">
#                 Estimated Market Value: {formatted_price}
#             </div>
#             """, unsafe_allow_html=True)
            
#             # Show input summary
#             with st.expander("Show Input Summary"):
#                 st.write("### Your Input Values")
#                 st.dataframe(input_data, hide_index=True)
                
#                 st.write("### Expected Features")
#                 st.write(feature_columns)
                
#         except Exception as e:
#             st.error(f"⚠️ Prediction Error: {str(e)}")
#             st.error("Please check your inputs and try again.")

# if __name__ == "__main__":
#     main()