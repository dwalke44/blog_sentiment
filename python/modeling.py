import configparser
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Embedding, Flatten, Dense

def fetch_all_training_data(dbpath:str, tbl_name:str):
    """
    Gets complete season of tokenized blog text for training in model
    """
    con = sqlite3.connect(f'{dbpath}')
    ocur = con.cursor()
    df = pd.DataFrame(ocur.execute(f"SELECT * FROM {tbl_name} order by gamedate;").fetchall())

    return df


if __name__ == "__main__":
    config = configparser.ConfigParser()
    # --------------------------------------------
    # config path for IDE dev
    config.read('sentiment/config/config.ini')
    # comment out when dev complete
    # ---------------------------------------------
    # config.read('config/config.ini')

    dbpath = config['DEFAULT']['dbpath']
    input_tbl_name = config['MODEL_OPS']['input_tbl']

    input_df = fetch_all_training_data(dbpath=dbpath, tbl_name=input_tbl_name)
    dates = input_df.iloc[:, 301].unique()

    for i in np.arange(0, dates):