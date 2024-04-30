
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import warnings
import os

import preprocessing
import evaluate
from collections import Counter

from typing import Dict
from sklearn.model_selection import train_test_split, KFold
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, precision_recall_curve, auc
from sklearn.pipeline import make_pipeline
import pickle

# Loading plotly packages for visualizations
import plotly.io as pio
pio.templates
import plotly.offline as py
from plotly.figure_factory import create_table

# Loading seaborn for visualization
import seaborn as sns

# Setting visualization parameters
matplotlib.rcParams['figure.figsize'] = (20, 10)
warnings.filterwarnings('ignore')

# Columns for categorical and numerical data
num_cols = ['tenure', 'monthlycharges', 'totalcharges']
cat_cols = [
    'gender', 'seniorcitizen', 'partner', 'dependents', 'phoneservice',
    'multiplelines', 'internetservice', 'onlinesecurity', 'onlinebackup',
    'deviceprotection', 'techsupport', 'streamingtv', 'streamingmovies',
    'contract', 'paperlessbilling', 'paymentmethod'
]

# Parameters for logistic regression model
params = {'solver': 'liblinear', 'random_state': 1, 'C': 0.5}


# Get the current directory (subfolder)
current_dir = os.path.dirname(__file__)

# Get the parent directory (project directory)
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))

# Construct the path to the data file in the parent directory
data_file_path = os.path.join(parent_dir, 'data', 'WA_Fn-UseC_-Telco-Customer-Churn.csv')

# Function to read data from CSV file
def get_data(filename: str) -> pd.DataFrame:
    data_frame = pd.read_csv(filename)
    return data_frame

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


def main():
    df = get_data(data_file_path)

   
    df = preprocess_data(df)

    
    

    print('succcessful 2')

    df_train_full, df_test = train_test_split(df, test_size=0.2, random_state=1)
    df_train_full = df_train_full.reset_index(drop=True)
    df_test = df_test.reset_index(drop=True)

    
    y_train = df_train_full.churn.values
    y_test = df_test.churn.values
    
    pipeline = make_pipeline(DictVectorizer(sparse=False), LogisticRegression(**params))


    del df_train_full['churn']
    
    print(Counter(y_train))
    print(Counter(y_test))
    
    
    pipeline.fit(preprocessing.get_dicts(df_train_full), y_train)
    
    del df_test['churn']
    y_pred = pipeline.predict_proba(preprocessing.get_dicts(df_test))[:, 1]

    evaluate.evaluate_model(y_pred, y_test)



    
    

if __name__ == "__main__":
    main()
