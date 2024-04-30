

from sklearn.metrics import roc_auc_score, precision_recall_curve, auc
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, KFold

from train import config
import preprocessing

from typing import List



def evaluate_model(y_pred: pd.DataFrame, y_test: pd.DataFrame):
    t = 0.5
    predict_churn = (y_pred >= t)
    predict_no_churn = (y_pred < t)
    actual_churn = (y_test == 1)
    actual_no_churn = (y_test == 0)
    
    true_positive = (predict_churn & actual_churn).sum()
    false_positive = (predict_churn & actual_no_churn).sum()
    false_negative = (predict_no_churn & actual_churn).sum()
    true_negative = (predict_no_churn & actual_no_churn).sum()


        
    confusion_table = np.array([[true_negative, false_positive], [false_negative, true_positive]])
    print(f'The confusion table {confusion_table}')

    Precision = true_positive / (true_positive + false_positive)
    print(f'The precision score is {Precision * 100}%')

    Recall = true_positive / (true_positive + false_negative)
    print(f'The Recall score is {Recall * 100} %')
    
    FPR = false_positive / (false_positive + true_negative)
    TPR = true_positive / (true_positive + false_negative)
    
    print(f'FPR is {FPR * 100}%')
    print(f'TPR is {TPR * 100}%')
    
    auc_score = roc_auc_score(y_test, y_pred)
    print(f'the auc score is {auc_score}')
    
    precision, recall, thresholds = precision_recall_curve(y_test, y_pred)
    auc_precision_recall = auc(recall, precision)
    print(f'the average precision score is {auc_precision_recall}')

    churn = y_pred >= 0.5

    acc = np.mean(y_test == churn)
    """ this means that 
    the model predictions matched
    the actual value 80% of the time."""

    print(f'the accuracy of the model is {acc}')


def run_KFOLD(data_frame: pd.DataFrame) -> List:

    kfold = KFold(n_splits=10, shuffle=True, random_state=1)
    
    aucs = []
    
    for train_idx, val_idx in kfold.split(data_frame):
        df_train = data_frame.iloc[train_idx]
        df_val = data_frame.iloc[val_idx]
        
        y_train = df_train.churn.values
        y_val = df_val.churn.values
        
        config.pipeline.fit(preprocessing.get_dicts(df_train), y_train)
        y_pred = config.pipeline.predict_proba(df_val[config.cat_cols + config.num_cols].to_dict(orient='records'))[:, 1]
        auc = roc_auc_score(y_val, y_pred)
        aucs.append(auc)
        aucs.sort(reverse=True)
        print('auc = %0.3f ± %0.3f' % (np.mean(aucs), np.std(aucs)))

    return aucs