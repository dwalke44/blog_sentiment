import sqlite3
import pandas as pd

"""
Connect to db
"""
con = sqlite3.connect('/Users/danwalker/Projects/Acipenser/database/nfl.db')
ocur = con.cursor()
sitemaps = pd.read_csv('~/Projects/Acipenser/database/acme_sitemaps.csv')
ocur.execute('CREATE TABLE ACME_SITEMAPS (sitemap_year_month)')
sitemaps.to_sql('ACME_SITEMAPS', con=con, if_exists='replace')

con.close()