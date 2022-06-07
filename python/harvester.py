import sqlite3
import configparser
import pandas as pd
import numpy as np
from selenium import webdriver
import selenium.common.exceptions as e
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


def scrape_url(url: str, selector_method: str, selector: str):
    """
    Takes a single URL, starts a Selenium sesh and scrapes elements defined by selector & method
    input: url
    input: selector_method: right now either ID or XPATH
    input: selector: input required for chosen selector method
    output: scraped_text: scraped text id'd by selector & method
    """

    # Ensure selector method is correct & formatted
    selector_method = selector_method.upper()
    valid_selector_methods = ['XPATH', 'ID']
    if selector_method not in valid_selector_methods:
        raise ValueError(f"Error: selector method must be one of {valid_selector_methods}")

    # Init selenium sesh
    options = Options()
    options.add_argument('--headless')
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:100.0) Gecko/20100101 Firefox/100.0")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    driver.get(url)
    # Start scraping
    if selector_method == 'XPATH':
        try:
            scraped_text = driver.find_element(by=By.XPATH, XPATH=selector).text
        except e.ElementNotSelectableException:
            print(f'Error: {e.ElementNotSelectableException}')
        except e.InvalidSelectorException:
            print(f'Error: {e.InvalidSelectorException}')
    elif selector_method == 'ID':
        try:
            scraped_text = driver.find_element(by=By.ID, ID=selector).text
        except e.ElementNotSelectableException:
            print(f'Error: {e.ElementNotSelectableException}')
        except e.InvalidSelectorException:
            print(f'Error: {e.InvalidSelectorException}')
    elif selector_method == 'CLASS':
        try:
            scraped_text = driver.find_element(by=By.CLASS_NAME, CLASS_NAME=selector).text
        except e.ElementNotSelectableException:
            print(f'Error: {e.ElementNotSelectableException}')
        except e.InvalidSelectorException:
            print(f'Error: {e.InvalidSelectorException}')
    driver.close()

    return scraped_text


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

    selector_meth = config['SCRAPER']['selector_method']
    selector = config['SCRAPER']['selector']

    for i in np.arange(0, guide_df.shape[0]):
        url = guide_df.loc[i][0]
        raw_text = scrape_url(url=url,
                              selector_method='ID',
                              selector=)

