"""
pad out game days to contain preceding weekdays
"""

import sqlite3
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import configparser


def pad_dates(gamedays, all_cal_days):
    out_df = pd.DataFrame(columns=['CALDATE', 'GAMEDATE'])
    for i in np.arange(0, len(gamedays)-1):
        gameday = gamedays.iloc[i, 0]
        if i == 0:
            cal_slice = all_cal_days[all_cal_days[0] <= gameday].copy()
            cal_slice['GAMEDATE'] = gameday
            cal_slice.columns = ['CALDATE', 'GAMEDATE']
            out_df = out_df.append(cal_slice, ignore_index=True)
        else:
            last_gameday = gamedays.iloc[i-1, 0]
            next_gameday = gamedays.iloc[i, 0]
            cal_slice = all_cal_days[(all_cal_days[0] > last_gameday) & (all_cal_days[0] <= next_gameday)].copy()
            cal_slice['GAMEDATE'] = gameday
            cal_slice.columns = ['CALDATE', 'GAMEDATE']
            out_df = out_df.append(cal_slice, ignore_index=True)

    return out_df


if __name__ == '__main__':
    cfg = configparser.ConfigParser()
    cfg.read('config/config.ini')
    con = sqlite3.connect(f'{cfg["DEFAULT"]["dbpath"]}')
    ocur = con.cursor()
    gamedays = pd.DataFrame(ocur.execute(f"SELECT distinct gameday FROM {cfg['LOCALDB']['result_tbl']};").fetchall())
    gamedays.columns = ['GAMEDAY']
    gamedays['GAMEWEEK_NUM'] = gamedays.index
    all_days = pd.date_range(start=datetime.strptime(gamedays['GAMEDAY'][0], '%Y-%m-%d')-timedelta(days=7),
                             end=gamedays['GAMEDAY'].max(), freq='d').strftime('%Y-%m-%d').to_frame()

    out = pad_dates(gamedays=gamedays, all_cal_days=all_days)

    out.to_sql(name=cfg['LOCALDB']['date_tbl'], con=con, if_exists='overwrite')


