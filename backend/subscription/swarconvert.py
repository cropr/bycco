# original Copyright Ruben Decrop
# modifications by Chessdevil Consulting BVBA

import logging
log = logging.getLogger(__name__)

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

def pairingsfromswar(swarjson):
    """
    get the pairings from the swarjson structure
    :param swarjson:
    :return:
    """
    (standings, pairings, bye, absences) = processswarjson(swarjson)
    skeys = sorted(pairings.keys())
    p = [pairings[k] for k in skeys]
    if bye:
        p.append(bye)
    p.extend(absences)
    return p

def standingsfromswar(swarjson):
    """
    get the pairings from the swarjson structure
    :param swarjson:
    :return:
    """
    (standings, pairings, bye, absences) = processswarjson(swarjson)
    skeys = sorted(standings.keys())
    s = [standings[k] for k in skeys]
    return s

def processswarjson(swarjson):
    """
    process the jsswarjson file calculating players and pairings
    standings, pairings, bye are dicts
    absences a list
    :param swarjson:
    :return: (standings, pairings, bye, absences)
    """
    pairings = {}
    standings = {}
    absences = []
    bye = None
    swar = swarjson.get('Swar')
    if not swar:
        log.debug('no swar file')
        return (standings, pairings, bye, absences)
    players = swar.get('Player')
    if not players:
        log.debug('no swar file')
        return (standings, pairings, bye, absences)
    for p in players:
        six = p.get('Ranking') - 1
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
            "tiebreak": p.get("TieBreak")
        }
        pl["rating"] = max(pl["natrating"], pl["fiderating"])
        ra = p.get("RoundArray")
        for ix, g in enumerate(ra):
            if len(ra) == ix + 1:
                standings[six] = pl
            round = g.get("RoundNr")
            if g.get("Tabel") == "Absent":
                pl["absences"].append({"round": int(round) -1})
                if len(ra) == ix + 1:
                    absences.append({
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
                if len(ra) == ix +1:
                    bye = {
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
            lastgame = {
                "table": int(g.get("Tabel")) - 1,
                "opponentIndex": g.get("OpponentNi"),
                "opponentName": g.get("OpponentName"),
                "result": g.get("Result").upper(),
                "color": "B" if g.get("Color") == "Black" else 'W',
                "float": g.get("Float"),
                "round": int(round)-1,
            }
            pl["games"].append(lastgame)
            if len(ra) == ix + 1:
                pix = lastgame["table"]
                lg = pairings.get(pix, {})
                if lastgame["color"] == "W":
                    lg["white"] =  pl["name"]
                    lg["white_id"] = pl["idbel"]
                    lg["white_rating"] = pl["rating"]
                    lg["white_points"] = pl["points"]
                    if lastgame["result"] == "1":
                        lg["result"] = "1-0"
                    elif lastgame["result"] == "½":
                        lg["result"] = "½-½"
                    elif lastgame["result"] == "0":
                        lg["result"] = "0-1"
                    elif lastgame["result"] == "1FF":
                        lg["result"] = "1-0 FF"
                    elif lastgame["result"] == "0FF":
                        lg["result"] = "0-1 FF"
                    else:
                        lg["result"] = " - "
                    pairings[pix] = lg
                if lastgame["color"] == "B":
                    lg["black"] = pl["name"]
                    lg["black_id"] = pl["idbel"]
                    lg["black_rating"] = pl["rating"]
                    lg["black_points"] = pl["points"]
                    pairings[pix] = lg
    return (standings, pairings, bye, absences)

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




