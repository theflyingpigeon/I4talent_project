import pandas as pd
import pickle
import xgboost as xgb

# Load the XGBoost model from the pickle file
model_path = 'models/XGBoost.sav'
with open(model_path, 'rb') as file:
    xgb_model = pickle.load(file)

# Define the feature names used during training
feature_names = [
    'leeftijd_begin_dienst', 'reisafstand', 'afdeling_Accountant',
    'afdeling_BI', 'afdeling_Boekhouder', 'afdeling_Business analist',
    'afdeling_Business controller', 'afdeling_Financial controller',
    'afdeling_IT', 'afdeling_Legal', 'afdeling_Marketing',
    'afdeling_Office manager', 'afdeling_Project controller',
    'afdeling_Administratief medewerker', 'afdeling_Business development',
    'afdeling_Credit controller', 'afdeling_HR', 'business_unit_Intern',
    'business_unit_Detachering', 'aantal_geboortes_pf'
]

# Load the new data for prediction from the CSV file
data_path = 'random_data.csv'
new_data = pd.read_csv(data_path)

column_order = ['leeftijd_begin_dienst', 'reisafstand', 'dienstperiode', 'aantal_geboortes_pf',
                'afdeling_Accountant', 'afdeling_Administratief medewerker', 'afdeling_BI',
                'afdeling_Boekhouder', 'afdeling_Business analist', 'afdeling_Business controller',
                'afdeling_Business development', 'afdeling_Credit controller', 'afdeling_Financial controller',
                'afdeling_HR', 'afdeling_IT', 'afdeling_Legal', 'afdeling_Marketing',
                'afdeling_Office manager', 'afdeling_Project controller', 'business_unit_Detachering',
                'business_unit_Intern']

new_data = new_data[column_order]
new_data = new_data.drop('dienstperiode', axis=1)

# Make predictions using the loaded model
predictions = xgb_model.predict(new_data)

# Display or use the predictions as needed
print("Predicted dienstperiode values:")
print(predictions)
