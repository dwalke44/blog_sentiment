import configparser
import pandas as pd
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
# from harvester import data_import, data_export
from sentiment.python.harvester import data_import, data_export



if __name__=='__main__':
    config = configparser.ConfigParser()
    # --------------------------------------------
    # config path for IDE dev
    # config.read('sentiment/config/config.ini')
    # comment out when dev complete
    # ---------------------------------------------
    config.read('config/config.ini')