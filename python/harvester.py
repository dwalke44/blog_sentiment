import sqlite3
import configparser
import time
import pandas as pd
import numpy as np
from datetime import datetime
from selenium import webdriver
import selenium.common.exceptions as e
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from nltk.corpus import stopwords
# from sentiment.python.text_ops import word_token_drop_sw, sort_filtered_text
from text_ops import word_token_drop_sw, sort_filtered_text


def data_import(dbpath, tbl_name):
    """
    Connects to SQL database and returns table given by tbl_name
    """
    con = sqlite3.connect(f'{dbpath}')
    ocur = con.cursor()
    df = pd.DataFrame(ocur.execute(f"SELECT * FROM {tbl_name};").fetchall())

    return df


def data_export(dbpath, df, tbl_name):
    """
    Export pandas dataframe to database
    """
    con = sqlite3.connect(f'{dbpath}')
    print(f'Exporting to database')
    df.to_sql(name=tbl_name, con=con, if_exists='append')


def selenium_session():
    # Init selenium sesh
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:100.0) Gecko/20100101 Firefox/100.0")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.delete_all_cookies()
    return driver


def scrape_url(url: str, selector_method: str, selector: str, driver: webdriver):
    """
    Takes a single URL, starts a Selenium sesh and scrapes elements defined by selector & method
    input: url
    input: selector_method: right now either ID or XPATH
    input: selector: input required for chosen selector method
    output: scraped_text: scraped text id'd by selector & method
    """

    # Ensure selector method is correct & formatted
    selector_method = selector_method.upper()
    valid_selector_methods = ['XPATH', 'ID', 'CLASS']
    if selector_method not in valid_selector_methods:
        raise ValueError(f"Selector method must be one of {valid_selector_methods}")

    driver.get(url)
    # Start scraping
    if selector_method == 'XPATH':
        scraped_text = driver.find_element(by=By.XPATH, value=f'{selector}').text
    elif selector_method == 'ID':
        scraped_text = driver.find_element(by=By.ID, value=f'{selector}').text
    elif selector_method == 'CLASS':
        scraped_text = driver.find_element(by=By.CLASS_NAME, value=f'{selector}').text
    driver.close()

    return scraped_text


if __name__ == "__main__":
    config = configparser.ConfigParser()
    # --------------------------------------------
    # config path for IDE dev
    # config.read('sentiment/config/config.ini')
    # comment out when dev complete
    # ---------------------------------------------
    config.read('config/config.ini')

    # Read in some required file names and locations
    dbpath = config['DEFAULT']['dbpath']
    urls_and_dates = config['LOCALDB']['urls_and_dates']
    output_tbl_name = config['LOCALDB']['output_table_name']
    embed_len = config['TEXT_OPS']['token_len']

    guide_df = data_import(dbpath=dbpath,
                           tbl_name=urls_and_dates)
    guide_df.columns = ['URL', 'PUB_DATE', 'GAME_DATE']

    selector_meth = config['SCRAPER']['selector_method']
    selector = config['SCRAPER']['selector']

    # Init stopwords dictionary to filter from raw text in preprocessing
    stop_words = set(stopwords.words('english'))
    text_lengths = []
    out_df = pd.DataFrame()
    start = datetime.now()
    print(f'Beginning web scraping & text processing at {start}')
    for i in np.arange(0, guide_df.shape[0]):
        url = guide_df.loc[i][0]
        gameday = guide_df.loc[i][2]
        try:
            driver = selenium_session()
            raw_text = scrape_url(url=url,
                                  selector_method=selector_meth,
                                  selector=selector,
                                  driver=driver)
        except e.ElementNotSelectableException:
            print(f'Error: {e.ElementNotSelectableException}')
        except e.InvalidSelectorException:
            print(f'Error: {e.InvalidSelectorException}')
        except e.TimeoutException:
            # Take a break & restart driver, reattempt URL if TimeoutError
            driver.close()
            time.sleep(10)
            try:
                driver = selenium_session()
                raw_text = scrape_url(url=url,
                                      selector_method=selector_meth,
                                      selector=selector,
                                      driver=driver)
            except e.TimeoutException:
                raw_text = np.nan
                continue
        except e.WebDriverException:
            # Take a break & restart driver, reattempt URL if TimeoutError
            driver.close()
            time.sleep(10)
            try:
                driver = selenium_session()
                raw_text = scrape_url(url=url,
                                      selector_method=selector_meth,
                                      selector=selector,
                                      driver=driver)
            except e.TimeoutException:
                raw_text = np.nan
                continue

        filt_text = word_token_drop_sw(raw_text=raw_text,
                                       stopwords_set=stop_words)
        # From KDE analysis, know that most tokens >= 250, all under 3318
        # DESIGN DECISION- call it 300 - pad shorter token lists, truncate longer
        top_n_words = sort_filtered_text(filtered_text=filt_text,
                                         desired_len=embed_len)
        print(f'Processing tokens from URL[{i}]')
        output = [url, gameday]
        for tup in top_n_words:
            output.append(tup[0])
        out = pd.Series(output).transpose()
        print(f'Saving to final dataframe')
        out_df.append(out, ignore_index=True)

    print(f'Exporting df of shape {out_df.shape} to database at {datetime.now()}')
    data_export(dbpath=dbpath, df=out_df, tbl_name=output_tbl_name)
    print(f'Scraping & processing of {guide_df.shape[0]} URLs completed at {datetime.now()-start}.')
