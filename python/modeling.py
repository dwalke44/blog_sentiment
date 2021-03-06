import os
import configparser
import math
import random
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import keras
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


def fetch_labeled_targets(dbpath:str, outcome_tbl:str):
    """
    Get game outcomes for season
    """
    con = sqlite3.connect(f'{dbpath}')
    ocur = con.cursor()
    df = pd.DataFrame(ocur.execute(f"SELECT TEAM_RESULT, gameday FROM {outcome_tbl};").fetchall())

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
    model.add(Dense(128, activation='linear'))
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
    outcomes = config['LOCALDB']['result_tbl']
    input_df = fetch_all_training_data(dbpath=dbpath, tbl_name=input_tbl_name)
    targets = fetch_labeled_targets(dbpath=dbpath, outcome_tbl=outcomes)
    dates = targets.iloc[:, 1]
    score = targets.iloc[:, 0]
    y_mean, y_std_dev, y = standardize_targets(targets=score)

    # Put model together
    # input_features = 300
    # output_feature = 1
    # 30 samples per timestep, 15 timesteps in total
    batch_size = 30
    timesteps = len(dates)
    max_len = int(config['TEXT_OPS']['token_len'])

    model = create_model_with_embed()
    # Save checkpoint for model
    checkpoint_path = "sentiment/output/models/checkpoints/training_1/cp.ckpt"
    checkpoint_dir = os.path.dirname(checkpoint_path)

    # Create a callback that saves the model's weights
    cp_callback = keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                  save_weights_only=True,
                                                  verbose=1)
    validation_output = pd.DataFrame()
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

        history = model.fit(X_train, y_train, batch_size=1, epochs=4,
                            validation_data=(X_test, y_test),
                            callbacks=[cp_callback])
        if i < len(dates)-1:
            X_valid = input_df[input_df.iloc[:, 301] == dates[i+1]]
            X_valid = X_valid.iloc[:, 1:301]
            y_valid = y[i+1]
            prediction = model.predict(X_valid).mean()
            valid_output = pd.Series([dates[i+1], y[i+1], y_mean, y_std_dev, prediction])
            validation_output = validation_output.append(valid_output, ignore_index=True)
        else:
            break
        print(f'Model trained for week of {dates[i]}. Iterating.')

    validation_output.columns = ['GAMEDAY', 'Y', 'Y_MEAN', 'Y_STD_DEV', 'Y_HAT']

    model.save_weights('sentiment/output/models/model1.h5')