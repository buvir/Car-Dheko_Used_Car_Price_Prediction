# 🚗 Car Dheko - Used Car Price Prediction

## Project Overview

This project aims to develop a robust machine learning model to predict used car prices and deploy it as an interactive [Streamlit](https://streamlit.io/) web application. The solution helps both customers and sales representatives at Car Dheko to get accurate price estimates quickly and easily.

---

## 📂 Project Structure

- `Final_Data_cleaning.ipynb` – Data cleaning, preprocessing, EDA, feature engineering, and model training notebook.
- `cars_encoded_StandardScaler.csv` – Cleaned and scaled dataset.
- `tuned_gb_model.pkl` – Final trained model (Gradient Boosting).
- `insurance_encoder.pkl`, `city_encoder.pkl`, `fuel_encoder.pkl`, `body_type_encoder.pkl` – Saved encoders for categorical features.
- `feature_columns.pkl` – List of features used for prediction.
- `model_metadata.json` – Metadata for Streamlit app (encoding orders, feature info).
- `streamlit_app.py` – Streamlit web application (to be created/deployed).
- `README.md` – Project documentation (this file).

---

## 🏷️ Features Used for Prediction

| Feature Name           | Description                                 | Type         |
|------------------------|---------------------------------------------|--------------|
| `KILOMETERS_DRIVEN`    | Total kilometers driven                     | Numerical    |
| `NUMBER_OF_OWNERS`     | Number of previous owners                   | Numerical    |
| `YEAR_OF_MANUFACTURE`  | Year the car was manufactured               | Numerical    |
| `MILEAGE`              | Mileage (km/l or equivalent)                | Numerical    |
| `NUMBER_OF_GEARS`      | Number of gears in the car                  | Numerical    |
| `SEATS`                | Number of seats                             | Numerical    |
| `INSURANCE_ENCODED`    | Insurance validity (ordinal encoded)        | Categorical  |
| `CITY_ENCODED`         | City (ordinal encoded)                      | Categorical  |
| `FUEL_TYPE_ENCODED`    | Fuel type (ordinal encoded)                 | Categorical  |
| `BODY_TYPE_ENCODED`    | Body type (label encoded)                   | Categorical  |
| `TRANSMISSION_ENCODED` | Transmission (0=Manual, 1=Automatic)        | Categorical  |

**Target Variable:**  
- `PRICE` – Selling price of the used car (numerical, scaled for modeling).

---

## 📈 Model

- **Algorithm:** Gradient Boosting Regressor (with hyperparameter tuning)
- **Evaluation Metrics:** MAE, RMSE, R²
- **Best Model:** Tuned Gradient Boosting (see notebook for details)
- **Why Regression?**  
  Regression is used because the target variable (price) is continuous and numerical.

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Car-Dheko_Used_Car_Price_Prediction.git
cd Car-Dheko_Used_Car_Price_Prediction
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Required Packages

```bash
pip install -r requirements.txt
```

If `requirements.txt` is missing, install manually:

```bash
pip install pandas numpy scikit-learn matplotlib seaborn streamlit joblib
```

---

## 🚀 Running the Streamlit App

After training and saving the model and encoders, launch the app with:

```bash
streamlit run streamlit_app.py
```

- Enter car details in the sidebar or form.
- Get instant price predictions and feature explanations.

---



Step by Step what i have done and saved csv 

1.all the cars csv's loaded
2.change and combined to csv_files/structured_cars_data.csv
3.Taken the necssary columns to csv_files/necessary_wanted_cols.csv
4.filled and removed  of 370 rows with blank and nan cars_filled_removed_final.csv
5.CLeaned and cleared all the data's example strip 5,00,000 to 500000 to cars_standard_final.csv
6.


## 📄 Documentation & Resources

- [Project Report & Methodology](docs/Project_Report.pdf) *(add your report here)*
- [Feature Description](docs/Feature_Description.md) *(add your feature doc here)*
- [Data Dictionary](docs/Data_Dictionary.md) *(add your data dictionary here)*
- [Model Evaluation Results](docs/Model_Evaluation.md) *(add your evaluation here)*
- [Streamlit User Guide](docs/Streamlit_User_Guide.md) *(add your user guide here)*

---

## 📝 Project Plan & Workflow

### 1. Data Collection and Preparation
- **Data Acquisition:** Download datasets from CarDekho for multiple cities.
- **Data Integration:** Import all city datasets, add 'City' column, concatenate into a single structured dataset.
- **Data Cleaning:** Handle missing values (imputation for numerical, mode/new category for categorical), standardize formats (remove units from strings, convert to proper data types), detect and handle outliers using IQR/Z-score methods.

### 2. Exploratory Data Analysis (EDA)
- **Descriptive Statistics:** Calculate central tendencies and dispersion metrics.
- **Visual Analysis:** Distribution plots, count plots, scatter plots, correlation heatmap.
- **Feature Analysis:** Identify most predictive features, analyze feature importance, detect multicollinearity.

### 3. Feature Engineering
- **Encoding:** One-hot encoding for nominal categorical variables, label/ordinal encoding for ordinal variables.
- **Scaling:** Apply Min-Max or Standard scaling for numerical features.
- **Feature Creation:** Calculate car age, create meaningful feature combinations.

### 4. Model Development
- **Train-Test Split:** 80-20 or 70-30 split with stratification.
- **Model Selection:** Linear Regression (baseline), Decision Trees, Random Forest, Gradient Boosting, Stacking/Ensemble methods.
- **Cross-Validation:** k-fold CV for robust evaluation.
- **Hyperparameter Tuning:** GridSearchCV/RandomizedSearchCV.

### 5. Model Evaluation
- **Metrics:** Primary: Mean Absolute Error (MAE); Secondary: MSE, RMSE, R².
- **Diagnostics:** Residual analysis, error distribution, feature importance plots.
- **Model Comparison:** Select best performing model based on metrics.

### 6. Deployment
- **Streamlit App Development:** User input forms for car features, real-time prediction display, explanatory visualizations, user-friendly interface.
- **Deployment Options:** Streamlit Sharing, AWS/GCP cloud deployment, Docker containerization.

### 7. Documentation and Reporting
- **Technical Documentation:** Data dictionary, methodology explanation, model selection rationale.
- **User Guide:** Instructions for using the Streamlit app.
- **Code Documentation:** PEP-8 compliant with clear comments.

---

## 🛠️ Technical Stack

- **Programming Language:** Python
- **Data Processing:** Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn, Plotly
- **Machine Learning:** Scikit-learn, XGBoost, LightGBM
- **Deployment:** Streamlit
- **Version Control:** Git/GitHub
- **Development Environment:** Jupyter Notebook, VS Code

---


## 📊 Success Metrics

- **Model Performance:** MAE < target threshold (to be determined from baseline)
- **Application Performance:** <2s response time for predictions
- **User Feedback:** Positive usability testing results

---

## 📢 Acknowledgements

- **Data Source:** [CarDekho](https://www.cardekho.com/)
- **Libraries:** Scikit-learn, Pandas, NumPy, Streamlit, Matplotlib, Seaborn

---

**Happy Predicting!**