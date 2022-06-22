import configparser
import math
import sqlite3
import pickle
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


def standardize_targets(targets):
    """
    Normalizes via z-score method target game outcomes for prediction
    """
    mean = sum(targets)/len(targets)
    var = sum(pow(x - mean, 2) for x in targets) / len(targets)
    std_dev = math.sqrt(var)
    output = []
    for x in targets:
        output.append((x-mean)/std_dev)

    return output

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
    targets = input_df.iloc[:, 302].unique()
    y = standardize_targets(targets=targets)
    # Get vocab pickle
    vocab_pickle = f"{config['TEXT_OPS']['pickle_jar']}/vocab.pickle"
    with open(vocab_pickle, 'rb') as inputfile:
        vocab = pickle.load(inputfile)

    # Put model together
    # input_features = 300
    # output_feature = 1
    # 30 samples per timestep, 15 timesteps in total
    batch_size = 30
    timesteps = len(dates)
    max_len = int(config['TEXT_OPS']['token_len'])

    model = Sequential()
    model.add(Embedding(10000, 64, input_length=max_len))
    model.add(Flatten())
    model.add(Dense(1, activation='linear'))
    model.compile(optimizer='rmsprop', loss='mape', metrics=['mae'])

    # Train model
    for i in np.arange(0, dates):
