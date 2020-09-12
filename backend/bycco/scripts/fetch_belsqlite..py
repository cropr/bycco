# Copyright 2017 Ruben Decrop

import datetime, urllib.request, sys, io
from bycco.service.sv_playerlist import process_zipsqlite_bel

def fetch_bel_sqlite():
    now = datetime.datetime.now()
    year = now.year
    month = (now.month - 1) // 3 * 3 + 1
    period = '{0:4d}{1:02d}'.format(year, month)
    print('period', period)
    url = f'http://www.frbe-kbsb.be/sites/manager/ELO/players_{period}.zip'
    try:
        f = urllib.request.urlopen(url)
    except urllib.request.URLError:
        print('Cannot open url %s', url)
        return False
    fdata = f.read()
    f.close()
    return process_zipsqlite_bel(io.BytesIO(fdata), period)


if __name__ == '__main__':
    print('fetching player.sqlite')
    if fetch_bel_sqlite():
        print('success')


