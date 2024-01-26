import pickle
import xgboost as xgb
import pandas as pd
import numpy as np
from sys import argv


def check_for_file() -> bool:
    try:
        if argv[1] != '':
            return True
        # TODO: check if file has all the columns
        return False
    except IndexError:
        return False


def read_file(filename: str) -> pd.DataFrame:
    df: pd.DataFrame = pd.read_csv(filename)
    return df


def ask_for_info() -> pd.DataFrame:
    df: pd.DataFrame = pd.read_csv('random_data.csv')
    return df


def predict_working_period(df: pd.DataFrame) -> None:
    model = pickle.load(open("models/XGBoost.sav", 'rb'))

    # Ensure the loaded model is an XGBoost regressor
    # if not isinstance(model, xgb.Booster):
    #     print("Error: The loaded model is not an XGBoost regressor.")
    #     return

    # Use the same features as used during training
    relevant_features = ['leeftijd_begin_dienst', 'reisafstand', 'afdeling_Accountant', 'afdeling_BI',
                         'afdeling_Boekhouder', 'afdeling_Business analist', 'afdeling_Business controller',
                         'afdeling_Financial controller', 'afdeling_IT', 'afdeling_Legal', 'afdeling_Marketing',
                         'afdeling_Office manager', 'afdeling_Project controller', 'business_unit_Detachering',
                         'afdeling_Administratief medewerker', 'afdeling_Business development',
                         'afdeling_Credit controller', 'afdeling_HR', 'business_unit_Intern',
                         'business_unit_Detachering', 'aantal_geboortes_pf']

    # Ensure the order of features in the DataFrame is the same as during training
    df = df[relevant_features]

    predictions = model.predict(df)
    print(f"Predictions: {predictions}")


if __name__ == '__main__':
    if check_for_file():
        df: pd.DataFrame = read_file(argv[1])
    else:
        df = ask_for_info()
    predict_working_period(df)
