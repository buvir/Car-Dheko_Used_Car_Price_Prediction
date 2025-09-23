# 📂 Data Folder

This folder stores all datasets used in the **Car Dheko Used Car Price Prediction** project.

---

## Structure

- **raw/**  
  Contains the original datasets collected from CarDekho for different cities.  
  Examples:  
  - `bangalore_cars.csv`  
  - `chennai_cars.csv`  
  - `delhi_cars.csv`  
  - `hyderabad_cars.csv`  
  - `jaipur_cars.csv`  
  - `kolkata_cars.csv`  

- **processed/**  
  Contains cleaned and combined datasets ready for analysis and model training.  
  Examples:  
  - `structured_cars_data.csv` → All city CSVs combined + city column added  
  - `final_cardekho_cleaned.csv` → Final cleaned dataset (used for model training)  
  - `cars_standard_final.csv` → Fully standardized dataset with formatting fixes  

---

## ⚠️ Note
- Large raw CSVs are **not tracked in Git** (they are ignored in `.gitignore`) to keep the repository lightweight.  
- Only the **processed/ready-to-train files** are tracked for reproducibility.  
- If you want to run the full pipeline, place raw datasets in `data/raw/` manually.  

---
