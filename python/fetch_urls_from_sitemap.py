import sqlite3
import requests
import pandas as pd
import numpy as np
import advertools as adv

"""
This script will parse a list of XML files from a website's sitemap to compile a list of URLs for scraping
"""


def fetch_sitemaps(dbpath):
    """
    Fetches manually-created list of sitemaps from local db
    """
    con = sqlite3.connect(f'{dbpath}')
    ocur = con.cursor()

    sitemaps = ocur.execute(f"SELECT * FROM GB_SITEMAPS;").fetchall()
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


def save_to_db():
