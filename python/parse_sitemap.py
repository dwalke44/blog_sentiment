import sqlite3
from argparse import ArgumentParser
import configparser
import pandas as pd
import advertools as adv
from datetime import datetime
from selenium import webdriver
import selenium.common.exceptions as e
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


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



if __name__ == '__main__':
    config = configparser.ConfigParser()
    # --------------------------------------------
    # config path for IDE dev
    config.read('sentiment/config/config.ini')
    # comment out when dev complete
    # ---------------------------------------------
    # config.read('config/config.ini')

    # Read in some required file names and locations
    dbpath = config['DEFAULT']['dbpath']
    # Get URL to be scraped
    parser = ArgumentParser(description='Get all blogs & their sitemaps from provided URL.')
    parser.add_argument('url', metavar='url', type=str, nargs='+',
                        help='web page to be scraped')
    args = parser.parse_args()
    url = args.url

    driver = selenium_session()
    driver.get(url=url)
    parents = driver.find_elements(by=By.CLASS_NAME, value=f'c-sports-blog-directory__item')
    links = driver.find_elements(by=By.TAG_NAME, value='a')
    item.find_element(by=By.TAG_NAME, value='a').text
    for item in links:
        print(item.get_attribute('href'))