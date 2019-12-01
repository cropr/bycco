# Copyright 2017 Ruben Decrop

import datetime, urllib.request, io
from bycco.service.sv_playerlist import read_zipfile_fide

def fetchplayerdbf():
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    period = '{0:4d}{1:02d}'.format(year, month)
    print('period', period)
    url = 'http://ratings.fide.com/download/players_list.zip'
    try:
        f = urllib.request.urlopen(url)
    except urllib.request.URLError:
        print('Cannot open url %s', url)
        return False
    fdata = f.read()
    f.close()
    return read_zipfile_fide(io.BytesIO(fdata), period)

if __name__ == '__main__':
    print('fetching fide standard rating list zipfile')
    if fetchplayerdbf():
        print('success')


