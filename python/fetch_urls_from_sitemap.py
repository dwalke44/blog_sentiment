import sqlite3
import pandas as pd
import numpy as np


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

