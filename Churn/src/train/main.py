import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import warnings
import os

import preprocessing

from collections import Counter



from typing import Dict
from sklearn.model_selection import train_test_split, KFold
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, precision_recall_curve, auc
from sklearn.pipeline import make_pipeline
import pickle

import train.data_manager as data_manager
import preprocessing
import train.config as config
import evaluate




# Parameters for logistic regression model


def main():
    try:

        df = data_manager.get_data(data_manager.data_file_path)


        df = preprocessing.preprocess_data(df)

        df_train_full, df_test = train_test_split(df, test_size=0.2, random_state=1)
        df_train_full = df_train_full.reset_index(drop=True)
        df_test = df_test.reset_index(drop=True)


        y_train = df_train_full.churn.values
        y_test = df_test.churn.values

        aucs = evaluate.run_KFOLD(df_train_full)

        if np.mean(aucs) > 0.835 and np.std(aucs) < 0.014:

            del df_train_full['churn']
            Pipeline = config.pipeline.fit(preprocessing.get_dicts(df_train_full), y_train)
                    
            del df_test['churn']
            y_pred = Pipeline.predict_proba(preprocessing.get_dicts(df_test))[:, 1]
            evaluate.evaluate_model(y_pred, y_test)
            
            with open(data_manager.model_path, 'wb') as file_out:
                 pickle.dump(Pipeline, file_out)

            print(f"Model saved to {data_manager.model_path}")
        else:
          print("Your model is below par")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
