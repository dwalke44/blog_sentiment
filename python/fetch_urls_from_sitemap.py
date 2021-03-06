import sqlite3
import configparser
import pandas as pd
import numpy as np
import advertools as adv
from datetime import datetime

"""
This script will parse a list of XML files from a website's sitemap to compile a list of URLs for scraping
"""


def fetch_sitemaps(dbpath, sm_tbl_name):
    """
    Fetches manually-created list of sitemaps from local db
    """
    con = sqlite3.connect(f'{dbpath}')
    ocur = con.cursor()

    sitemaps = ocur.execute(f"SELECT * FROM {sm_tbl_name};").fetchall()
    sitemaps_s = []
    for i in np.arange(0, len(sitemaps)):
        sitemaps_s.append(sitemaps[i][1])
    sitemaps_out = pd.Series(sitemaps_s)
    ocur.close()
    con.close()
    return sitemaps_out


def fetch_single_xml(sitemap_url):
    """
    Uses advertools' sitemap_to_df fxn to parse single XML
    """
    content_df = adv.sitemap_to_df(sitemap_url)

    return content_df


def save_to_db(dbpath, sitemap_url_df, output_tbl_name):
    """
    Appends extracted URLs from processed sitemap to db table
    """
    con = sqlite3.connect(f'{dbpath}')
    sitemap_url_df.to_sql(f'{output_tbl_name}', con=con, if_exists='replace')
    con.close()


if __name__ == '__main__':
    # Read in config
    config = configparser.ConfigParser()
    config.read('sentiment/config/config.ini')

    # Collect sitemap keys
    source_url = config['DEFAULT']['sitemap_source']
    sitemaps = fetch_single_xml(source_url)
    save_to_db(dbpath=config['DEFAULT']['dbpath'],
               sitemap_url_df=sitemaps,
               output_tbl_name=config['LOCALDB']['url_tbl_name'])
