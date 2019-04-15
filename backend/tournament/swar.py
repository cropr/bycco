# Copyright Ruben Decrop 2012 - 2019

import logging
log = logging.getLogger(__name__)

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
import simplejson as json
import functools


from .models import (
    CdSwarTournament,
    CdSwarJson,
    CdSwarPairings,
    CdSwarStandings,
    CdTournament,
    CdTournamentPrizes,
    Subscription,
)

from .serializers import (
    ParticipantSerializer,
    SubscriptionSerializer,
    SwarTournamentSerializer,
    SwarJsonSerializer,
    SwarJsonSerializerSmall,
    TournamentSerializer,
    UploadSwarJsonSerializer,
)


def playercardfromswar(swarjson, plix):
    """
    return the player card for a single player
    :param swarjson: 
    :param plix: the player index
    :return: 
    """
    swar = swarjson.get('Swar')
    if not swar:
        log.debug('no swar file')
        return None
    players = swar.get('Player')
    if not players:
        log.debug('no swar file')
    for p in players:
        ix  = p.get("Ni", -1)
        if ix != plix:
            continue
        return dict(player=p)
    log.debug("No player found for index %d", plix)
    return None

def pairingsfromswar(swarjson, round):
    """
    get the pairings from the swarjson structure
    :param swarjson:
    :return:
    """
    try:
        p =  CdSwarPairings.objects.get(
            round=round, swartrn=swarjson.swartrn).jsonpairings
        return json.loads(p)
    except CdSwarPairings.DoesNotExist:
        return None

def standingsfromswar(swarjson, round):
    """
    get the pairings from the swarjson structure
    :param swarjson:
    :return:
    """
    try:
        p =  CdSwarStandings.objects.get(
            round=round, swartrn=swarjson.swartrn).jsonstandings
        return json.loads(p)
    except CdSwarPairings.DoesNotExist:
        return None


def comparestanding(s1, s2):
    """ compare function to sort standings"""
    if s1['points'] > s2['points']: return -1
    if s1['points'] < s2['points']: return 1
    if s1['ni'] > s2['ni']: return -1
    if s1['ni'] < s2['ni']: return 1
    return 0    

def processSwarJsonFile(swar):
    """
    process the jsswarjson file calculating players and pairings
    write jsonfied string to CdSwarPairing and CdSwarStanding
    for all rounds found 
    :param swar: {CdSwarJson} 
    :return: None
    """
    pairings = {}
    standings = {}
    absences = {}
    bye = {}
    swj = json.loads(swar.jsonfile)
    maxround = 0
    players = swj.get('Swar').get('Player')
    if not players:
        log.debug('no swar file')
        return (standings, pairings, bye, absences)
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
    for round in range(1, maxround+1):
        try:
            swp = CdSwarPairings.objects.get(round=round, 
                swartrn=swar.swartrn)
        except CdSwarPairings.DoesNotExist:
            swp = CdSwarPairings(round=round, swartrn=swar.swartrn)
        result = [ pairings[round][k] for k in sorted(pairings[round].keys()) ]
        if bye[round]:
            result.append(bye[round])
        result.extend(absences[round])
        swp.jsonpairings = json.dumps(result)
        swp.save()
        try:
            sws = CdSwarStandings.objects.get(round=round, 
                swartrn=swar.swartrn)
        except CdSwarStandings.DoesNotExist:
            sws = CdSwarStandings(round=round, swartrn=swar.swartrn)
        result = sorted(standings[maxround].values(), key=lambda p: p['rank']) 
        sws.jsonstandings = json.dumps(result)
        sws.save()


prizetable = {
    'BG8': ([60, 50, 40, 30, 20], [50,	30]),
    'B10': ([70, 65, 61, 56, 52, 47, 43, 38, 34, 29, 25, 20],[]),
    'G10': ([], [70, 53, 37, 20]),
    'B12': ([80, 77,	73,	70,	67,	63,	60,	57,	53,	50,	47,	43,	40,	37,	33,	30,	27,	23,	20], []),
    'G12': ([], [80, 65, 50, 35, 20]),
    'B14': ([110, 105, 99, 94, 89, 84, 78, 73, 68, 62, 57, 52, 46, 41, 36, 31, 25, 20], []),
    'G14': ([], [110, 88, 65, 43, 20]),
    'B16': ([140, 131, 122, 112, 103, 94, 85, 75, 66, 57, 48, 38, 29, 20], []),
    'G16': ([], [120, 80, 40]),
    'BG18': ([150, 138, 126, 115, 103, 91, 79, 67, 55, 44, 32, 20], [130]),
    'BG20': ([160, 137, 113, 90, 67, 43, 20], [140, 40]),
}

def generate_code():
    from random import randint
    code = randint(1,9999999)
    dig31 = code // 10000
    dig32 = (code - (dig31 * 10000)) // 10
    dig33 = (code % 10) * 100 + code % 97
    return "{0:03d}-{1:03d}-{2:03d}".format(dig31, dig32, dig33)

def prizesfromswar(swarjson, category):
    """
    return the player card for a single player
    :param swarjson: 
    :param plix: the player index
    :return: 
    """
    (standings, pairings, bye, absences) = processswarjson(swarjson)
    skeys = sorted(standings.keys())
    playerprizes = []
    curmix = 0
    curfix = 0
    prizes = prizetable[category]
    for k in skeys:
        prizem = prizes[0][curmix] if curmix < len(prizes[0]) else None
        prizef = prizes[1][curfix] if curfix < len(prizes[1]) else None
        player = standings[k]
        if player['gender'] == 'M' and prizem:
            playerprizes.append({
                'name': player['name'],
                'category': category,
                'place': curmix+1,
                'prize': prizem,
                'code': generate_code(),
                'gender': 'M',
            })
            curmix += 1
            continue
        if player['gender'] == 'F' and prizef:
            if prizem and prizem > prizef:
                prizef = prizem
                log.debug('girl is taking boys price')
            playerprizes.append({
                'name': player['name'],
                'category': category,
                'place': curfix+1,
                'prize': prizef,
                'code': generate_code(),
                'gender': 'F',
            })
            curfix += 1
            continue
    return dict(playerprizes=playerprizes)

# swar
@api_view(['GET', 'POST'])
def swartrn_all(request):

    if request.method == 'POST':
        # adding a new swar file
        uploadSerializer = UploadSwarJsonSerializer(data=request.data)
        if not uploadSerializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        uploadSwar = uploadSerializer.validated_data
        id_trn = uploadSwar['id_trn']
        name = uploadSwar['name']
        jsonfile = uploadSwar['jsonfile']
        round = uploadSwar['round']
        try:
            trn = CdTournament.objects.get(id=id_trn)
        except CdTournament.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            swartrn = CdSwarTournament.objects.get(tournament=trn)
        except CdSwarTournament.DoesNotExist:
            # no swartrn exists, so create it
            swartrn = CdSwarTournament(tournament=trn, swarname=name)
            swartrn.save()
        swarjson = CdSwarJson(round=round, jsonfile=jsonfile, swartrn=swartrn)
        swarjson.save()
        return Response(status=status.HTTP_201_CREATED)

    if request.method == 'GET':
        swardata = {}
        for swartrn in CdSwarTournament.objects.all():
            srl = SwarTournamentSerializer(swartrn)
            swardata[swartrn.tournament_id] = srl.data
        for trn in CdTournament.objects.all():
            if trn.id in swardata:
                swardata[trn.id].update(TournamentSerializer(trn).data)
        return Response(dict(swartrns=swardata.values()))

@api_view(['GET', 'DELETE'])
def swartrn_one(request, id_trn):
    try:
        trn = CdSwarTournament.objects.get(tournament_id=id_trn)
    except CdSwarTournament.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        trn_serializer = SwarTournamentSerializer(trn)
        return Response(trn_serializer.data)

    if request.method == 'DELETE':
        trn.delete()
        trns = CdSwarTournament.objects.all()
        trn_serializer = SwarTournamentSerializer(trns, many=True)
        return Response(trn_serializer.data)

@api_view(['POST'])
def swarfile_publication(request, id_swartrn, id_swarfile):
    try:
        CdSwarTournament.objects.get(tournament_id=id_swartrn)
    except CdSwarTournament.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    try:
        swar = CdSwarJson.objects.get(id=id_swarfile)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    processSwarJsonFile(swar)
    CdSwarJson.objects.filter(swartrn_id=id_swartrn, status='ACT',
                              round=swar.round).update(status='OUT')
    CdSwarJson.objects.filter(swartrn_id=id_swartrn, id=id_swarfile).update(
        status='ACT')
    return Response(status=status.HTTP_201_CREATED)

@api_view(['GET'])
def swarfile_all(request, id_swartrn):

    try:
        swartrn = CdSwarTournament.objects.get(tournament_id=id_swartrn)
    except CdSwarTournament.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    swarjsons = CdSwarJson.objects.filter(swartrn_id=id_swartrn).order_by(
                '-round', '-uploaddate')
    ss = SwarJsonSerializerSmall(swarjsons, many=True)
    return Response(ss.data)

@api_view(['GET', 'DELETE'])
def swarfile_one(request, id_swartrn, id_swarfile):

    try:
        swar = CdSwarJson.objects.get(swartrn_id=id_swartrn, id=id_swarfile)
    except CdSwarJson.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        ss = SwarJsonSerializer(swar)
        return Response(ss.data)

    if request.method == 'DELETE':
        swar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

