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

xlsx_order: list[str] = ['name', 'Predicted working period']


def create_input_file() -> None:
    columns: list[str] = ['name']
    for column in column_order:
        columns.append(column)
    column_dataframe: pd.DataFrame = pd.DataFrame(columns=columns)
    column_dataframe.to_excel('Predictions/Sample_input_file.xlsx', index=False)


def check_file() -> bool:
    # Check if someone passed in a potential filename and if it is a file
    try:
        if os.path.exists(argv[1]):
            if argv[1].lower().endswith(('.csv', '.xlsx', '.xls')):
                return True
            else:
                exit('Please use a CSV, XLSX or XLS file 2')
        else:
            return False
    except IndexError:
        exit('No file has been given!')


def check_columns(check_df: pd.DataFrame) -> pd.DataFrame:
    # Check if the dataframe has all the columns
    check_df = check_df.reindex(columns=column_order, fill_value=False)

    # Remove the dienstperiode column
    check_df = check_df.drop('name', axis=1, errors='ignore')
    check_df = check_df.drop('dienstperiode', axis=1, errors='ignore')

    return check_df


def run_prediction() -> None:
    # Read the different filetypes
    if argv[1].lower().endswith('csv'):
        df = pd.read_csv(argv[1])
    elif argv[1].lower().endswith('xlsx') or argv[1].lower().endswith('xls'):
        df = pd.read_excel(argv[1])
    else:
        exit("Could not read file")

    predicted_df = check_columns(df)

    # Load the model and make a prediction
    xgb_model = pickle.load(open('models/XGBoost.sav', 'rb'))
    predictions = xgb_model.predict(predicted_df)
    predicted_df['Predicted working period'] = predictions
    predicted_df['Predicted working period'] = predicted_df['Predicted working period'].astype(int)

    # Add the name column to the predicted database
    predicted_df['name'] = df['name']

    # Remove the unwanted/unneeded cells and update the column order
    predicted_df.drop(columns=column_order, inplace=True, errors='ignore')
    predicted_df = predicted_df.reindex(columns=xlsx_order)

    # Save the working period to a csv and Excel file
    predicted_df.to_csv(f'Predictions/predicted {datetime.now().day} - {datetime.now().month}.csv', sep=',',
                        index=False)
    predicted_df.to_excel(f'Predictions/predicted.xlsx', sheet_name=f'{datetime.now().day} - {datetime.now().month}',
                          index=False)


if __name__ == '__main__':
    if check_file():
        run_prediction()
    elif len(argv) == 1:
        create_input_file()
        print("A template has been created")
    else:
        exit('Please input a CSV, XLSX or XLS file')
