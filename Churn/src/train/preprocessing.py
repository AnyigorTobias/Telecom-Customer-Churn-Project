from typing import List, Dict

import pandas as pd
num_cols = ['tenure', 'monthlycharges', 'totalcharges']
cat_cols = [
    'gender', 'seniorcitizen', 'partner', 'dependents', 'phoneservice',
    'multiplelines', 'internetservice', 'onlinesecurity', 'onlinebackup',
    'deviceprotection', 'techsupport', 'streamingtv', 'streamingmovies',
    'contract', 'paperlessbilling', 'paymentmethod'
]


def get_dicts(data_frame: pd.DataFrame) -> List[Dict]:

    data = data_frame[cat_cols + num_cols].to_dict('records')

    return data



def preprocess_data(data_frame: pd.DataFrame) -> pd.DataFrame:
    # Converting 'TotalCharges' column to numeric datatype
    data_frame["TotalCharges"] = pd.to_numeric(data_frame['TotalCharges'], errors="coerce")

    # Drop 'customerID' column
    data_frame = data_frame.drop(columns=['customerID'])

    # Converting 'SeniorCitizen' column to categorical 'Yes'/'No'
    data_frame['SeniorCitizen'] = data_frame['SeniorCitizen'].apply(lambda x: 'No' if x == 0 else 'Yes')
    
    # Dropping rows with missing values
    data_frame = data_frame.dropna()

    # Converting column headers to lowercase and replacing spaces with underscores
    data_frame.columns = data_frame.columns.str.lower().str.replace(' ', '_')

    # Converting 'churn' column values to integers (1 for 'Yes', 0 for 'No')
    
    data_frame['churn'] = (data_frame['churn'] == 'Yes').astype(int)
    
    return data_frame
