import configparser
import sqlite3
import pickle
import pandas as pd
import numpy as np
from collections import Counter
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
from keras.layers import TextVectorization
from keras.models import Sequential
# from harvester import data_import, data_export
from sentiment.python.harvester import data_import, data_export
from sentiment.python.text_ops import convert_samples_to_model_input

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
    full_df = pd.DataFrame(ocur.execute(f'SELECT * FROM {db_tbl} where "1" = "{gameday}" ORDER BY "0";').fetchall())
    sampled_df = full_df.sample(n=num_samples, axis=0)
    return sampled_df


def get_outcomes(result_tbl: str, dbpath: str):
    """
    Get game day and outcomes for prediction
    """
    con = sqlite3.connect(f'{dbpath}')
    ocur = con.cursor()
    df = pd.DataFrame(ocur.execute(f'SELECT GB.GAMEDAY, GB.GB_RESULT FROM {result_tbl} GB WHERE GB.SEASON = 2021;')
                      .fetchall())

    return df


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
    vocab_pickle = f"{config['DEFAULT']['pickle_jar']}/vocab.pickle"
    # Get guiding index - gameday dates
    dates = fetch_gamedays(input_tbl=date_tbl,
                           dbpath=dbpath)
    # Get dependent variable & gamedate
    results = config['LOCALDB']['result_tbl']

    results = get_outcomes(result_tbl=results,
                           dbpath=dbpath)

    for i in np.arange(0, len(dates)):
        # Read in and sample tokens to form standardized input
        gameday = dates[0][i]
        sample = fetch_standardized_tokens(gameday=gameday,
                                           db_tbl=date_tbl,
                                           dbpath=dbpath,
                                           num_samples=num_urls_per_sample)
        sample.fillna(value='Empty', inplace=True)

        # Reconstitute string of top 300 words per blog per gameday
        tokens_only = sample.iloc[:, 3:sample.shape[1]]
        labels = sample.iloc[:, 1:3]
        concat_samples = pd.DataFrame(dtype=str)
        # Takes all 30 blog posts & concats into single string per blog post
        for j in np.arange(0, tokens_only.shape[0]):
            single_pg = tokens_only.iloc[j, :].to_list()
            s = pd.Series(' '.join(single_pg))
            concat_samples = concat_samples.append(s, ignore_index=True)

        # Use counter to convert strings to counts of occurrence & update vocabulary
        if [config]['DEFAULT']['first_run']:
            # Init vocab for first manual run, but this object needs to be persisted and updated as learning from blogs
            # goes on
            vocab = Counter()
            vocab, sequences = convert_samples_to_model_input(cleaned_samples=concat_samples,
                                                              counter_vocabulary=vocab)
            # Export vocab as pickle
            with open(vocab_pickle, 'wb') as outputfile:
                pickle.dump(vocab, outputfile)
        else:
            # Get vocab pickle
            with open(vocab_pickle, 'rb') as inputfile:
                vocab = pickle.load(inputfile)
            vocab, sequences = convert_samples_to_model_input(cleaned_samples=concat_samples,
                                                              counter_vocabulary=vocab)


        # Modeling
        vectorize_layer = TextVectorization(output_mode='int')

        # Call `adapt` on the text-only dataset to create the vocabulary.
        vectorize_layer.adapt(concat_samples)

        # Create the model that uses the vectorize text layer
        model = Sequential()
