# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging

import json, io, zipfile, sys
import dbf
from datetime import datetime, date
from flask import render_template, abort
from werkzeug.exceptions import NotFound
from typing import List, Optional, Union, Tuple
from bycco import app
from bycco.models import BelplayerModel, FideplayerModel, SubscriptionModel

log = logging.getLogger('bycco')

def getBelplayer(id: str) -> Tuple[BelplayerModel, bool]:
    """
    get the page by id amd return is player is a;ready registered
    """
    log.info(f'getting belplayer by id {id}')
    bp = BelplayerModel.find_by_id(id)
    bp.currentratingbel = bp.currentrating()
    try:
        ss = SubscriptionModel.find_by_idbel(id)
        alreadyregistered = True
    except NotFound:
        alreadyregistered = False
    return (bp, alreadyregistered)

def read_zipfile_bel(fszip, period):
    """
    reads the ratinglist zipfile, decrompress it and store all active
    players in the belranking collection
    :param fszip: byte stream of the zipfile
    :param period: the period in yyyymm format of the ranking file
    :return: None
    """

    # read the first file in zipfile  and convert it to a byte stream
    zf = zipfile.ZipFile(fszip, mode='r')
    zfd = zf.open(zf.namelist()[0])
    pldata = zfd.read()
    zfd.close()
    plbindata = io.BytesIO(pldata)

    # create a dbf file from the byte stream
    players = dbf.Dbf()
    players.openOn(plbindata)
    print('player.dbf contains {0:d} records'.format(len(players)))

    i = 0
    dot = 0

    # read every dbase record
    for row in range(len(players)):
        try:
            line = players[row]
        except:
            print('dbf read error for line %d', row)
            return False
        if line["SUPPRESS"]:    # don't add deleted players
            continue
        bel_id = str(line['MATRICULE'])
        try:
            p = BelplayerModel.find_by_id(bel_id)
        except NotFound:
            p = BelplayerModel.blank(bel_id)
        if ',' in line['NOM_PRENOM']:  # new format as of 2015
            nfn = line['NOM_PRENOM'].split(',')
            p.first_name = nfn[1].strip()
            p.last_name = nfn[0].strip()
        else:
            nfn = line['NOM_PRENOM'].split()
            p.first_name = nfn.pop().capitalize()
            p.first_name = ' '.join([s.capitalize() for s in nfn])
        p.gender = line['SEXE']
        year, month, day = line['DATE_NAISS']
        if year == 0:
            year, month, day = (1900, 1, 1)
        p.birthdate = date(year, month, day).isoformat()
        p.idclub = str(line['CLUB'])
        idfide = line['FIDE']
        p.idfide = str(idfide) if idfide else ""
        p.federation = line['FEDERATION']
        p.nationalitybel = line['NOUV_MOD']
        belrating = line['ELO_CALCUL']
        for r in p.ratingsbel:
            if r['period'] == period:
                r['rating'] = belrating
                break
        else:
            p.ratingsbel.append({
                'period': period,
                'rating': belrating,
            })
        i += 1
        dot += 1
        if dot == 100:
            print(',', end='')
            sys.stdout.flush()
            dot = 0
        p.save()
    print('\n{0:d} players created to belplayer'.format(i))
    return True

def getFideplayer(id: str) -> FideplayerModel:
    """
    get the page by id 
    """
    log.info(f'getting fideplayer by id {id}')
    fp = FideplayerModel.find_by_id(id)
    fp.currentratingfide = fp.currentrating()
    return fp

def read_zipfile_fide(fszip, period):
    """
    reads the ratinglist zipfile, decrompress it and store all active
    players in the fideranking collection
    :param fszip: byte stream of the zipfile
    :param period: the period in yyyymm format of the ranking file
    :return: None
    """

    # read the first file in zipfile  and convert it to a byte stream
    zf = zipfile.ZipFile(fszip, mode='r')
    plist = zf.open(zf.namelist()[0])

    # skip first line with headers
    plist.readline()


    dot = 0

    # read every line
    for i, row in enumerate(plist):
        line = row.decode('utf-8')
        fide_id = line[0:15].strip()
        try: 
            p = FideplayerModel.find_by_id(fide_id)
        except NotFound:
            p = FideplayerModel.blank(fide_id)
        nfn = line[15:76].split(',')
        p.last_name = nfn[0].strip()
        p.first_name = nfn[1].strip() if len(nfn) == 2 else ''
        p.nationalityfide = line[76:79]
        p.gender = line[80]
        p.birthyear = line[152:156]
        p.chesstitle = line[84:88].strip()
        fiderating = int(line[113:117].strip() or 0)
        for r in p.ratingsfide:
            if r['period'] == period:
                r['rating'] = fiderating
                break
        else:
            p.ratingsfide.append({
                'period': period,
                'rating': fiderating,
            })
        dot += 1
        if dot == 1000:
            print(',', end='')
            sys.stdout.flush()
            dot = 0
        p.save()
    zf.close()
    print('\n{0:d} players created to fideplayer'.format(i))
    return True
