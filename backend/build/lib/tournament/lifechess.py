# all rights reserved
# original copyright by Ruben Decrop
# modifications by Chessdevil Consulting BVBA

import simplejson as json
import os, os.path
import datetime

board_configs = [
    {
        'venue': 'U8',
        'boards': [
            {'group': 'U8', 'board': 1},
            {'group': 'U8', 'board': 2},
            {'group': 'U8', 'board': 3},
            {'group': 'U8', 'board': 4},
            {'group': 'U8', 'board': 5},
        ]
    },
    {
        'venue': 'B10',
        'boards': [
            {'group': 'B10', 'board': 1},
            {'group': 'B10', 'board': 2},
            {'group': 'B10', 'board': 3},
            {'group': 'B10', 'board': 4},
            {'group': 'B10', 'board': 5},
            {'group': 'B10', 'board': 6},
            {'group': 'B10', 'board': 7},
            {'group': 'B10', 'board': 8},
            {'group': 'B10', 'board': 9},
            {'group': 'B10', 'board': 10},
            {'group': 'B10', 'board': 11},
            {'group': 'B10', 'board': 12},
        ]
    },
    {
        'venue': 'G10',
        'boards': [
            {'group': 'G10', 'board': 1},
            {'group': 'G10', 'board': 2},
        ]
    },
    {
        'venue': 'B12',
        'boards': [
            {'group': 'B12', 'board': 1},
            {'group': 'B12', 'board': 2},
            {'group': 'B12', 'board': 3},
            {'group': 'B12', 'board': 4},
            {'group': 'B12', 'board': 5},
            {'group': 'B12', 'board': 6},
            {'group': 'B12', 'board': 7},
            {'group': 'B12', 'board': 8},
            {'group': 'B12', 'board': 9},
            {'group': 'B12', 'board': 10},
            {'group': 'B12', 'board': 11},
            {'group': 'B12', 'board': 12},
            {'group': 'B12', 'board': 13},
            {'group': 'B12', 'board': 14},
            {'group': 'B12', 'board': 15},
            {'group': 'B12', 'board': 16},
            {'group': 'B12', 'board': 17},
            {'group': 'B12', 'board': 18},
            {'group': 'B12', 'board': 19},
        ]
    },
    {
        'venue': 'G12',
        'boards': [
            {'group': 'G12', 'board': 1},
            {'group': 'G12', 'board': 2},
            {'group': 'G12', 'board': 3},
            {'group': 'G12', 'board': 4},
            {'group': 'G12', 'board': 5},
            {'group': 'G12', 'board': 6},            
        ]
    },
    {
        'venue': 'B14',
        'boards': [
            {'group': 'B14', 'board': 1},
            {'group': 'B14', 'board': 2},
            {'group': 'B14', 'board': 3},
            {'group': 'B14', 'board': 4},
            {'group': 'B14', 'board': 5},
            {'group': 'B14', 'board': 6},
            {'group': 'B14', 'board': 7},
            {'group': 'B14', 'board': 8},
            {'group': 'B14', 'board': 9},
            {'group': 'B14', 'board': 10},
            {'group': 'B14', 'board': 11},
            {'group': 'B14', 'board': 12},
            {'group': 'B14', 'board': 13},
            {'group': 'B14', 'board': 14},
            {'group': 'B14', 'board': 15},
            {'group': 'B14', 'board': 16},
            {'group': 'B14', 'board': 17},
            {'group': 'B14', 'board': 18},
            {'group': 'B14', 'board': 19},
            {'group': 'B14', 'board': 20},
        ]
    },
    {
        'venue': 'G14',
        'boards': [
            {'group': 'G14', 'board': 1},
            {'group': 'G14', 'board': 2},
            {'group': 'G14', 'board': 3},
            {'group': 'G14', 'board': 4},
        ]
    },
    {
        'venue': 'B16',
        'boards': [
            {'group': 'B16', 'board': 1},
            {'group': 'B16', 'board': 2},
            {'group': 'B16', 'board': 3},
            {'group': 'B16', 'board': 4},
            {'group': 'B16', 'board': 5},
            {'group': 'B16', 'board': 6},
            {'group': 'B16', 'board': 7},
            {'group': 'B16', 'board': 8},
            {'group': 'B16', 'board': 9},
            {'group': 'B16', 'board': 10},
            {'group': 'B16', 'board': 11},
            {'group': 'B16', 'board': 12},
            {'group': 'B16', 'board': 13},
            {'group': 'B16', 'board': 14},
        ]
    },
    {
        'venue': 'G16',
        'boards': [
            {'group': 'G16', 'board': 1},
            {'group': 'G16', 'board': 2},
            {'group': 'G16', 'board': 3},
            {'group': 'G16', 'board': 4},
            {'group': 'G16', 'board': 5},
            {'group': 'G16', 'board': 6},
            {'group': 'G16', 'board': 7},
        ]
    },
    {
        'venue': 'B18',
        'boards': [
            {'group': 'B18', 'board': 1},
            {'group': 'B18', 'board': 2},
            {'group': 'B18', 'board': 3},
            {'group': 'B18', 'board': 4},
            {'group': 'B18', 'board': 5},
            {'group': 'B18', 'board': 6},
            {'group': 'B18', 'board': 7},
            {'group': 'B18', 'board': 8},
            {'group': 'B18', 'board': 9},
            {'group': 'B18', 'board': 10},
            {'group': 'B18', 'board': 11},
            {'group': 'B18', 'board': 12},
            {'group': 'B18', 'board': 13},
        ]
    },
    {
        'venue': 'G18',
        'boards': [        
            {'group': 'G18', 'board': 1},
            {'group': 'G18', 'board': 2},
            {'group': 'G18', 'board': 3},
            {'group': 'G18', 'board': 4},
        ]
    },
    {
        'venue': 'U20',
        'boards': [
            {'group': 'U20', 'board': 1},
            {'group': 'U20', 'board': 2},
            {'group': 'U20', 'board': 3},
            {'group': 'U20', 'board': 4},
            {'group': 'U20', 'board': 5},
            {'group': 'U20', 'board': 6},
            {'group': 'U20', 'board': 7},
            {'group': 'U20', 'board': 8},
            {'group': 'U20', 'board': 9},
        ]
    },
    {
        'venue': 'IMT',
        'boards': [
            {'group': 'IMT', 'board': 1},
            {'group': 'IMT', 'board': 2},
            {'group': 'IMT', 'board': 3},
            {'group': 'IMT', 'board': 4},
            {'group': 'IMT', 'board': 5},
        ]
    },    
]

swar2019 = [
    ("BJK CBJ 2019 -08BG.json", "U8"),
    ("BJK CBJ 2019 -10B.json", "B10"),
    ("BJK CBJ 2019 -10G.json", "G10"),
    ("BJK CBJ 2019 -12B.json", "B12"),
    ("BJK CBJ 2019 -12G.json", "G12"),
    ("BJK CBJ 2019 -14B.json", "B14"),
    ("BJK CBJ 2019 -14G.json", "G14"),
    ("BJK CBJ 2019 -16B.json", "B16"),
    ("BJK CBJ 2019 -16G.json", "G16"),
    ("BJK CBJ 2019 -18B.json", "B18"),
    ("BJK CBJ 2019 -18G.json", "G18"),
    ("BJK CBJ 2019 -20BG.json", "U20"),
    ("IM-normentoernooi op het BJK 2019.json", "IMT"),
]

testlife = [
    ("BJK CBJ 2019 -20BG.json", "U20"),    
]

def load_tournaments(trns):
    """
    Loads the json files generated by SWAR 
    Returns:
        dict -- all the parsed tournaments, indexed by group
    """
    trn = {}
    for filename, group in trns:
        path = os.path.join( os.getcwd(), 'data', filename)
        with open(path, 'rb') as f:
            trn[group] =  json.load(f)
    return trn

def lookup_game(trn, round, board):
    """
    lookup a game in a tournament
    Arguments:
        trn {dict} -- the tournament
        round {integer} -- round number human
        board {integer} -- board number human
    Returns:
        tuple -- (whiteplayer, blackplayer) or None
    """
    white = None
    black = None
    for player in trn['Swar']['Player']:
        for pairing in player['RoundArray']:
            if pairing['RoundNr'] == round and pairing['Tabel'] == str(board):
                if pairing['Color'] == "White":
                    white = player
                    break
                if pairing['Color'] == 'Black':
                    black = player
                    break
    return (white, black) if white and black else None

def generate_lifechess_pgns(bc, trns, round):
    """
    Generates the content of the pgn file for livechess boards for a
    single venue
    Arguments:
        bc {dict} -- a board config for the single venue
        trns {dict} -- all the tournament files indexed by group
        round {int} -- the round number as human 
    Returns:
        str -- the generated pgn for all games in venue
    """
    pgns = [] 
    for b in bc['boards']:
        trn = trns.get(b['group'])
        if not trn:
            print('could not find tournament for group', b['group'])
            pgns.append(pgn_from_game(None, b['group'], round)) 
            continue
        game = lookup_game(trn, round, b['board'])
        if not game:
            print('Could not find game', b['group'], round, 
                b['board'])
        pgns.append(pgn_from_game(game, b['group'], round)) 
    return b'\n\n'.join(pgns)

def pgn_from_game(game, group, round):
    """
    creates an empty pgn from a game
    attention is given to encoding as pgn requires latin-1
    Arguments:
        game {tuple} -- whiteplayer,blackplayer or None
        group {str} -- the category in the tournament
        round {int} -- the round number as human
    Returns:
        str -- the pgn fro a single game
    """
    if game:
        white = game[0]['Name']
        black = game[1]['Name']
    else:
        white = '?'
        black = '?'
    return b"""[Event "Belgian Youth championships 2019 %(group)b"]
[Site "Blankenberge, Belgium BEL"]
[Date "%(today)b"]
[Round "%(round)d"]
[White "%(white)b"]
[Black "%(black)b"]
[Result "*"]

*
""" % {
    b'group': group.encode('latin-1'),
    b'today': datetime.date.today().strftime("%Y.%m.%d").encode('latin-1'),
    b'round': round,
    b'white': white.encode('utf-8'),
    b'black': black.encode('utf-8')
}

def dump_pgn(pgns):
    for i, bc in enumerate(board_configs):
        with open("{0}.pgn".format(bc['venue']), 'wb') as f:
            f.write(pgns[i])

if __name__ == "__main__":
    trns = load_tournaments(swar2019)
    # trns = load_tournaments(testlife)
    round = 1
    pgns = [generate_lifechess_pgns(bc, trns, round) for bc in board_configs]
    dump_pgn(pgns)
    print('wrote pgn files for round', round)
