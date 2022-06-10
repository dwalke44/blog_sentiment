import sqlite3
import configparser
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sentiment.python.harvester import data_import

config = configparser.ConfigParser()
config.read(f'sentiment/config/config.ini')

df = data_import(dbpath=config['DEFAULT']['dbpath'],
                 tbl_name=config['LOCALDB']['output_table_name'])

df.head()
