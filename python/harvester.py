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


def scrape_url(url, xpath):
    """
    Takes a single URL, starts a Selenium sesh and scrapes text id'd by give XPath
    """
    options = Options()
    options.add_argument('--headless')
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:100.0) Gecko/20100101 Firefox/100.0")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    driver.get(url)
    scraped_text = driver.find_element(by=By.XPATH, xpath=xpath).text


if __name__ == "__main__":
    config = configparser.ConfigParser()
    # --------------------------------------------
    # config path for IDE dev
    config.read('sentiment/config/config.ini')
    # comment out when dev complete
    # ---------------------------------------------
    config.read('config/config.ini')

    # Read in some required file names and locations
    dbpath = config['DEFAULT']['dbpath']
    urls_and_dates = config['LOCALDB']['urls_and_dates']

    guide_df = data_import(dbpath=dbpath,
                           tbl_name=urls_and_dates)
    guide_df.columns = ['URL', 'PUB_DATE', 'GAME_DATE']

