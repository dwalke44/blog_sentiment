import sqlite3
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


"""
Import dates to inform scraping
"""
con = sqlite3.connect('/Users/danwalker/Projects/Acipenser/database/nfl.db')
ocur = con.cursor()
date_tbl = f'GB_DATES_2021'
date_sheet = pd.DataFrame(ocur.execute(f'SELECT * FROM {date_tbl};'))
date_sheet_cols = ocur.execute(f"SELECT name FROM PRAGMA_TABLE_INFO('{date_tbl}');").fetchall()
date_sheet_cols_s = []
for i in np.arange(0, len(date_sheet_cols)):
    date_sheet_cols_s.append(date_sheet_cols[i][0])
# print(date_sheet_cols_s)
date_sheet.columns = date_sheet_cols_s
# print(date_sheet.head())

"""
Init chromedriver session
"""
options = Options()
options.add_argument('--headless')
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:100.0) Gecko/20100101 Firefox/100.0")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")







