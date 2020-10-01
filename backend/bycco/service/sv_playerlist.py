# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging

import json, io, zipfile, sys
from datetime import datetime, date
from typing import List, Optional, Union, Tuple
from bycco.models.md_playerlist import Belplayer, Fideplayer
from bycco.crud.db_playersqlite import get_belplayer, get_fideplayer
from reddevil.common import RdBadRequest, RdNotFound

log = logging.getLogger('bycco')

def getBelplayer(id: str) -> Belplayer:
    """
    get the player 
    """
    log.info(f'getting belplayer by id {id}')
    try:
        i = int(id)
    except:
        raise RdBadRequest(description='InvalidBelId')
    rec = get_belplayer(i)
    if not rec:
        raise RdNotFound(description='BelplayerNotFound')
    names = rec['Name'].split(', ')
    if len(names) > 1:
        last_name, first_name = names[0:2]
    else:
        last_name, first_name = names[0], ''
    return Belplayer(
        affiliated = rec['Affiliated'] == 1,
        birthdate = rec['Birthday'],
        federation = rec['Fed'],
        first_name = first_name,
        gender = rec["Sex"],
        id = id,  
        idclub = rec["Club"],
        idfide = str(rec['FideId']),
        last_name = last_name,
        nationality =  rec["NatFideSign"],
        ratingbel = rec["Elo"]
    )

def process_zipsqlite_bel(fszip, period):
    """
    reads the ratinglist zipfile, decrompress it and store it as sqlite lite file on the server
    :param fszip: byte stream of the zipfile
    :param period: the period in yyyymm format of the ranking file
    :return: None
    """

    # read the first file in zipfile  and convert it to a byte stream
    with zipfile.ZipFile(fszip, mode='r') as zf:
        zfd = zf.open(zf.namelist()[0])
        pldata = zfd.read()
        zfd.close()
    with open('data_bycco/players.sqlite', 'wb') as fs:
        fs.write(pldata)


def getFideplayer(id: str) -> Optional[Fideplayer]:
    """
    get the page by id 
    """
    log.info(f'getting fideplayer by id {id}')
    if not id:
        return None
    try:
        i = int(id)
    except:
        raise RdBadRequest(description='InvalidFideId')
    rec = get_fideplayer(i)
    if not rec:
        raise RdNotFound(description='FideplayerNotFound')
    names = rec['Name'].split(', ')
    if len(names) > 1:
        last_name, first_name = names[0:2]
    else:
        last_name, first_name = names[0], ''
    return Fideplayer(
        birthyear = rec["BDay"],
        chesstitle = rec["Tit"] or '',
        first_name = first_name,
        gender = rec["Sex"],
        last_name = last_name,
        nationality = rec['Fed'],
        ratingfide = rec["SRtng"]
    )

def process_zipsqlite_fide(fszip):
    """
    reads the ratinglist zipfile, decrompress it and store all active
    players in the fideranking collection
    :param fszip: byte stream of the zipfile
    :return: None
    """
    with zipfile.ZipFile(fszip, mode='r') as zf:
        zfd = zf.open(zf.namelist()[0])
        pldata = zfd.read()
        zfd.close()
    with open('data_bycco/fide.sqlite', 'wb') as fs:
        fs.write(pldata)