import sqlite3
import configparser
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def data_import(dbpath, tbl_name):
    """
    Connects to SQL database and returns table given by tbl_name
    """
    con = sqlite3.connect(f'{dbpath}')
    ocur = con.cursor()
    df = pd.DataFrame(ocur.execute(f"SELECT * FROM {tbl_name};").fetchall())

    return df


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config/config.ini')

    # Read in some required file names and locations
    dbpath = config['DEFAULT']['dbpath']
    urls_and_dates = config['LOCALDB']['urls_and_dates']

    guide_df = data_import(dbpath=dbpath,
                           tbl_name=urls_and_dates)
    guide_df.columns = ['URL', 'PUB_DATE', 'GAME_DATE']
    print(guide_df.head())

