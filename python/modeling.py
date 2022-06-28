import os
import configparser
import math
import random
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Embedding, Flatten, Dense

random.seed(865)


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

    return mean, std_dev, output


def create_model_with_embed():
    """
    Creates keras sequential model including embedding layer
    """

    model = Sequential()
    model.add(Embedding(10000, 64, input_length=max_len))
    model.add(Flatten())
    model.add(Dense(64, activation='linear'))
    model.add(Dense(1, activation='linear'))
    model.compile(optimizer='rmsprop', loss='mape', metrics=['mae'])

    return model



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
    y_mean, y_std_dev, y = standardize_targets(targets=targets)

    # Put model together
    # input_features = 300
    # output_feature = 1
    # 30 samples per timestep, 15 timesteps in total
    batch_size = 30
    timesteps = len(dates)
    max_len = int(config['TEXT_OPS']['token_len'])

    model = create_model_with_embed()

    # Train model
    for i in np.arange(0, len(dates)):
        print(f'Training model for week {dates[i]}')
        X = input_df[input_df.iloc[:, 301] == dates[i]]
        X = X.iloc[:, 1:301]
        X_train = X.sample(n=25)
        X_test = X.drop(X_train.index)
        X_train = X_train.to_numpy()
        X_test = X_test.to_numpy()
        y_train = pd.Series(y[i], index=np.arange(0, X_train.shape[0]), name='y').to_numpy()
        y_test = pd.Series(y[i], index=np.arange(0, X_test.shape[0]), name='y').to_numpy()

        history = model.fit(X_train, y_train, batch_size=1, epochs=10,
                            validation_data=(X_test, y_test))
        print(f'Model trained for week of {dates[i]}. Iterating.')
    model.save_weights('sentiment/output/models/model1.h5')
