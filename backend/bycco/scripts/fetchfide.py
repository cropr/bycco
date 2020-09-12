# Copyright 2017 Ruben Decrop

import datetime, urllib.request, io
from bycco.service.sv_playerlist import process_zipsqlite_fide

def fetch_fide_sqlite():
    url = f'https://www.frbe-kbsb.be/sites/manager/ELO/fide.sqlite.zip'
    try:
        f = urllib.request.urlopen(url)
    except urllib.request.URLError:
        print('Cannot open url %s', url)
        return False
    fdata = f.read()
    f.close()
    return process_zipsqlite_fide(io.BytesIO(fdata))

if __name__ == '__main__':
    print('fetching fide standard rating list zipfile')
    if fetch_fide_sqlite():
        print('success')
