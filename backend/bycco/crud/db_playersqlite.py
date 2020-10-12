# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

# all database requests come in here, but we do not use dataclasess
# no business logic in here, just plain database queries
# every record is returned as a dict

import sqlite3
import logging

log = logging.getLogger('bycco')

belconn = sqlite3.connect('data_bycco/players.sqlite')
fideconn = sqlite3.connect('data_bycco/fide.sqlite')

belfields = [
    "idNumber", "Name", "Sex", "Birthday", "Fed", "Club", "Affiliated",
    "Elo", "EloPrevious", "Gain", "Games", "GamesPrevio", "Performance",
    "Opponents", "LastGames", "Border", "Arbiter", "NatPlayer", "NatFideSign",
    "G", "Died", "FideId", "LoginModif", "DateModif"
]

def get_belplayer(id: int):
    c = belconn.cursor()
    c.execute('SELECT * FROM players WHERE idNumber=?', (id,))
    rs = c.fetchone()
    # log.info(f'rs {rs}')
    return {i[0]:i[1] for i in zip(belfields, rs)}

fidefields = [
    "IdNumber", "Name", "Fed", "Sex", "Tit", "WTit", "OTit", "FOA", "SRtng", 
    "SGm", "SK", "RRtng", "RGm", "Rk", "BRtng", "BGm", "BK", "BDay", 
    "Flag", "Birthday",
]

def get_fideplayer(id: int):
    c = fideconn.cursor()
    c.execute('SELECT * FROM fide WHERE idNumber=?', (id,))
    return {i[0]:i[1] for i in zip(fidefields, c.fetchone())}
