# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import logging

import json, os.path, io, csv
from typing import List, Optional, Dict, Any, Tuple, cast
from datetime import date, datetime, timezone
from bycco.service.sv_playerlist import getBelplayer, getFideplayer
from reddevil.common import RdInternalServerError
from bycco.service.mail import sendconfirmationmail

from bycco.models.md_swar import (
    RoundPublication,
    SwarJsonIn,
    SwarTrnIn,
    SwarTrnOut,
    SwarTrnList,
)
from bycco.crud.db_swar import DbSwar
from reddevil.common import RdNotFound, RdBadRequest

log = logging.getLogger('bycco')

def encode_swartrn(e: dict, cls=SwarTrnOut):
    try:
        o = cls(**e)
    except Exception:
        log.exception(f'cannot encode {cls.__name__}')
        raise RdInternalServerError(description='CannotEncodeSwarTrnOut')
    return o

async def addSwarTrn(sti: SwarTrnIn) -> str:
    """
    add a new swar tournament
    """
    st = sti.dict()
    st['swarname'] = ''
    st['swarjsons'] = {}
    return await DbSwar.add(st)

async def addSwarJsonFile(si: SwarJsonIn) -> None:
    """
    add a new swar json file
    """
    st = await getSwarTrn(si.idswar)
    pairings, standings = processSwarJsontext(si.jsontext)
    sj = {
        'jsontext': si.jsontext,
        'pairings': pairings,
        'standings': standings,
        'status': RoundPublication.Unpublished
    }
    await DbSwar.update({'id': si.idswar}, {
        'swarname': si.swarname,
        f'swarjsons.{si,round}': sj
    })

async def deleteSwarTrn(id: str) -> None:
    await DbSwar.delete(id)

async def getSwarTrns(options: dict={}, cls=SwarTrnOut) -> SwarTrnList:
    """
    get all swartrn
    """
    sdict = await DbSwar.find_multiple(options)
    return SwarTrnList(trns= [encode_swartrn(s, cls) for s in sdict])

async def getSwarTrn(id: str, options: dict= {}, cls=SwarTrnOut) -> SwarTrnOut:
    """
    get one swartrn,
    """
    filter = dict(id=id, **options)
    sdict = await DbSwar.find_single(filter)
    return encode_swartrn(sdict, cls)

def processSwarJsontext(swarjsontext: str) -> Tuple[Dict[int, str], Dict[int, str]]:
    """
    process the swar jsontext calculating players and pairings
    write jsonfied string to CdSwarPairing and CdSwarStanding
    for all rounds found 
    return a tuple(parings, s)
    """
    pairings: Dict[int, dict] = {}
    standings: Dict[int, dict] = {}
    absences: dict = {}
    bye: dict = {}
    swj = json.loads(swarjsontext)
    maxround = 0
    players = swj.get('Swar').get('Player')
    if not players:
        log.debug('no swar file')
        return (standings, pairings)
    for p in players:
        six = p.get('Ranking')
        pl = {
            "name": p.get('Name'),
            "id_player": p.get("Ni"),
            "points": float(p.get("Points")),
            "gender": "F" if p.get("Sex").startswith('F') else 'M',
            "country": p.get("Country"),
            "idbel": str(p.get("NationalId")),
            "id_fide": str(p.get("FideId")),
            "id_club": str(p.get("ClubNumber")),
            "tpr": str(p.get("Performance")),
            "clubname": p.get("ClubName"),
            "natrating": p.get("NationalElo", 0),
            "fiderating": p.get("FideElo", 0),
            "titel": p.get("Titel"),
            "ngames": p.get("NbOfParts"),
            "games": [],
            "bye": None,
            "absences": [],
            "tiebreak": p.get("TieBreak"),
            "rank": six,
            "ni": p.get("Ni"),
        }
        pl["rating"] = max(pl["natrating"], pl["fiderating"])
        ra = p.get("RoundArray")
        for ix, g in enumerate(ra):
            round = g.get("RoundNr")
            if round > maxround:
                maxround = round
            if not round in standings:
                standings[round] = {}
                pairings[round] = {}
                absences[round] = []
                bye[round] = None
            round = g.get("RoundNr")
            standings[round][six] = pl
            if g.get("Tabel") == "Absent":
                pl["absences"].append({"round": round -1})
                absences[round].append({
                    "white": pl["name"],
                    "white_id": pl["idbel"],
                    "white_rating": pl["rating"],
                    "white_points": pl["points"],
                    "result": "--",
                    "black": "",
                    "black_id": "",
                    "black_rating": '',
                    "black_points": '',
                })
                continue
            if g.get("Tabel") == "BYE":
                pl["bye"] = {"round": int(round) -1}
                bye[round] = {
                    "white": pl["name"],
                    "white_id": pl["idbel"],
                    "white_rating": pl["rating"],
                    "white_points": pl["points"],
                    "result": "Bye",
                    "black": "",
                    "black_id": "",
                    "black_rating": '',
                    "black_points": '',
                }
                continue
            game = {
                "table": int(g.get("Tabel")),
                "opponentIndex": g.get("OpponentNi"),
                "opponentName": g.get("OpponentName"),
                "result": g.get("Result").upper(),
                "color": "B" if g.get("Color") == "Black" else 'W',
                "float": g.get("Float"),
                "round": round - 1,
            }
            pix = game["table"]
            lg = pairings[round].get(pix, {})
            if game["color"] == "W":
                lg["white"] =  pl["name"]
                lg["white_id"] = pl["idbel"]
                lg["white_rating"] = pl["rating"]
                lg["white_points"] = pl["points"]
                if game["result"] == "1":
                    lg["result"] = "1-0"
                elif game["result"] == "½":
                    lg["result"] = "½-½"
                elif game["result"] == "0":
                    lg["result"] = "0-1"
                elif game["result"] == "1FF":
                    lg["result"] = "1-0 FF"
                elif game["result"] == "0FF":
                    lg["result"] = "0-1 FF"
                else:
                    lg["result"] = " - "
                pairings[round][pix] = lg
            if game["color"] == "B":
                lg["black"] = pl["name"]
                lg["black_id"] = pl["idbel"]
                lg["black_rating"] = pl["rating"]
                lg["black_points"] = pl["points"]
                pairings[round][pix] = lg
    log.info('pairings in round 1: %d %d', len(pairings[1]), maxround) 
    jsonpairings = {}
    jsonstandings = {}
    for round in range(1, maxround+1):
        result = [ pairings[round][k] for k in sorted(pairings[round].keys()) ]
        if bye[round]:
            result.append(bye[round])
        result.extend(absences[round])
        jsonpairings[round] = json.dumps(result)
        result = sorted(standings[maxround].values(), key=lambda p: p['rank']) 
        jsonstandings[round] = json.dumps(result)
