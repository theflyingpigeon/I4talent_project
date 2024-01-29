from datetime import datetime
import pandas as pd
import pickle
import os
from sys import argv, exit

column_order = ['leeftijd_begin_dienst', 'reisafstand', 'dienstperiode', 'aantal_geboortes_pf',
                'afdeling_Accountant', 'afdeling_Administratief medewerker', 'afdeling_BI',
                'afdeling_Boekhouder', 'afdeling_Business analist', 'afdeling_Business controller',
                'afdeling_Business development', 'afdeling_Credit controller', 'afdeling_Financial controller',
                'afdeling_HR', 'afdeling_IT', 'afdeling_Legal', 'afdeling_Marketing',
                'afdeling_Office manager', 'afdeling_Project controller', 'business_unit_Detachering',
                'business_unit_Intern']


def check_file() -> bool:
    # Check if someone passed in a potential filename and if it is a file
    try:
        if os.path.exists(argv[1]):
            return True
        else:
            return False
    except IndexError:
        exit('No file has been given!')


def check_columns(df: pd.DataFrame) -> pd.DataFrame:
    # Check if the dataframe has all the columns
    df = df.reindex(columns=column_order, fill_value=False)

    # Remove the dienstperiode column
    df = df.drop('dienstperiode', axis=1, errors='ignore')

    return df


if __name__ == '__main__':
    if not check_file():
        exit("Could not find the provided csv file")
    df: pd.DataFrame = pd.read_csv(argv[1])
    df = check_columns(df)

    # Load the model and make a prediction
    xgb_model = pickle.load(open('models/XGBoost.sav', 'rb'))
    predictions = xgb_model.predict(df)
    df['Predicted working period'] = predictions

    # Remove the unwanted/unneeded cells
    columns_to_drop: list[str] = ['afdeling_Accountant', 'afdeling_Administratief medewerker', 'afdeling_BI',
                'afdeling_Boekhouder', 'afdeling_Business analist', 'afdeling_Business controller',
                'afdeling_Business development', 'afdeling_Credit controller', 'afdeling_Financial controller',
                'afdeling_HR', 'afdeling_IT', 'afdeling_Legal', 'afdeling_Marketing',
                'afdeling_Office manager', 'afdeling_Project controller', 'business_unit_Detachering',
                'business_unit_Intern']

    df.to_csv(f'Predictions/predicted {datetime.now().day} - {datetime.now().month}.csv', sep=',', index=False)
    df.to_excel(f'Predictions/predicted.xlsx', sheet_name=f'{datetime.now().day} - {datetime.now().month}')
