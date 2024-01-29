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
            if argv[1].lower().endswith('.csv'):
                return True
            else:
                exit('Please use a CSV file')
        else:
            return False
    except IndexError:
        exit('No file has been given!')


def check_columns(check_df: pd.DataFrame) -> pd.DataFrame:
    # Check if the dataframe has all the columns
    check_df = check_df.reindex(columns=column_order, fill_value=False)

    # Remove the dienstperiode column
    check_df = check_df.drop('dienstperiode', axis=1, errors='ignore')

    return check_df


if __name__ == '__main__':
    # Check if the file exist
    if not check_file():
        exit("Could not find the provided csv file")

    # Set the df variable equal to all the data in the csv file
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
    df.drop(columns=columns_to_drop, inplace=True, errors='ignore')

    # Save the working period to a csv and Excel file
    df.to_csv(f'Predictions/predicted {datetime.now().day} - {datetime.now().month}.csv', sep=',', index=False)
    df.to_excel(f'Predictions/predicted.xlsx', sheet_name=f'{datetime.now().day} - {datetime.now().month}', index=False)
