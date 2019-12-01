# Copyright 2017 Ruben Decrop

import datetime, urllib.request, sys, io
from bycco.service.sv_playerlist import read_zipfile_bel

def fetchplayerdbf():
    now = datetime.datetime.now()
    year = now.year
    month = (now.month - 1) // 3 * 3 + 1
    period = '{0:4d}{1:02d}'.format(year, month)
    print('period', period)
    url = 'http://www.frbe-kbsb.be/sites/manager/ELO/PLAYER_{0}.ZIP'.format(
        period)
    try:
        f = urllib.request.urlopen(url)
    except urllib.request.URLError:
        print('Cannot open url %s', url)
        return False
    fdata = f.read()
    f.close()
    return read_zipfile_bel(io.BytesIO(fdata), period)


if __name__ == '__main__':
    print('fetching player.dbf')
    if fetchplayerdbf():
        print('success')


