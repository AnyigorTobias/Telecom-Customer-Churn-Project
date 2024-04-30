
import pandas as pd
import os
from train import config




filename = config.filename



def get_data(filename: str) -> pd.DataFrame:
    data_frame = pd.read_csv(filename)
    return data_frame
