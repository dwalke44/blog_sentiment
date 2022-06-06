import sqlite3
import requests
import pandas as pd
import numpy as np

"""
This script will parse a list of XML files from a website's sitemap to compile a list of URLs for scraping
Follows the tutorial at: https://www.geeksforgeeks.org/xml-parsing-python/
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

    return sitemaps_out


def get_links_from_sitemap_xml(sitemap_url):
    """
    Parses a single XML file for the URLs embedded therein
    """
    payload = requests.get(sitemap_url)
    content = payload.text
    return content