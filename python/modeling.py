import configparser
import sqlite3
import pandas as pd
import numpy as np
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
# from harvester import data_import, data_export
from sentiment.python.harvester import data_import, data_export


def fetch_gamedays(input_tbl: str, dbpath: str):
    """
    Gets gamedays from target table
    """
    con = sqlite3.connect(f'{dbpath}')
    ocur = con.cursor()
    df = pd.DataFrame(ocur.execute(f'SELECT DISTINCT "1" FROM {input_tbl};').fetchall())

    return df


def fetch_standardized_tokens(gameday: str, db_tbl: str, dbpath: str, num_samples: int):
    """
    Fetches data for gameday & returns df of sampled number of URLs
    Sample of URLS: different numbers of blogs per gameday, but have to standardize to minimum bc
        neural nets require standardized input shapes
    """
    con = sqlite3.connect(f'{dbpath}')
    ocur = con.cursor()
    full_df = pd.DataFrame(ocur.execute(f'SELECT * FROM {db_tbl} where "1" = "{gameday}";').fetchall())
    sampled_df = full_df.sample(n=num_samples, axis=0)
    return sampled_df


if __name__ == '__main__':
    config = configparser.ConfigParser()
    # --------------------------------------------
    # config path for IDE dev
    config.read('sentiment/config/config.ini')
    # comment out when dev complete
    # ---------------------------------------------
    # config.read('config/config.ini')
    dbpath = config['DEFAULT']['dbpath']
    date_tbl = config['LOCALDB']['urls_dates_tokens']
    num_urls_per_sample = int(config['MODEL_OPS']['num_urls_per_sample'])

    dates = fetch_gamedays(input_tbl=date_tbl,
                           dbpath=dbpath)
    for i in np.arange(0, len(dates)):
        # Read in and sample tokens to form standardized input
        gameday = dates[0][i]
        sample = fetch_standardized_tokens(gameday=gameday,
                                           db_tbl=date_tbl,
                                           dbpath=dbpath,
                                           num_samples=num_urls_per_sample)
