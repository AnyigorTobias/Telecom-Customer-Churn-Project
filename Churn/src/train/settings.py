import os
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression

from path import current_dir, parent_dir

# Columns for categorical and numerical data
num_cols = ['tenure', 'monthlycharges', 'totalcharges']
cat_cols = [
    'gender', 'seniorcitizen', 'partner', 'dependents', 'phoneservice',
    'multiplelines', 'internetservice', 'onlinesecurity', 'onlinebackup',
    'deviceprotection', 'techsupport', 'streamingtv', 'streamingmovies',
    'contract', 'paperlessbilling', 'paymentmethod'
]

filename = 'WA_Fn-UseC_-Telco-Customer-Churn.csv'

params = {'solver': 'liblinear', 'random_state': 1, 'C': 0.5}


pipeline = make_pipeline(DictVectorizer(sparse=False), LogisticRegression(**params))

model_name = "classification_model.pkl"
output_dir = "../output"  # Navigate up one directory to reach the churn folder

# Ensure that the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Construct the full path to save the model
model_path = os.path.join(output_dir, model_name)




