# all rights reserved
# original copyright by Ruben Decrop
# modifications by Chessdevil Consulting BVBA

import simplejson as json
import sys

def loadtrnjson():
    with open('BJK CBJ 2018 -16 Girls.json') as f:
        a = json.load(f)
    return a

def fixtrn(trn, round):
    swar  = trn['Swar']
    players = swar['Player']
    for p in players:
        p['NbRounds'] = round
        p['RoundArray'] = [ x for i,x in enumerate(p['RoundArray']) if i < round]
    return trn

def dumptrn(trn, round):
    with open('BJK CBJ 2018 -16 Girls r{0:d}.json'.format(round), 'w') as f:
        json.dump(trn, f, indent="  ")

if __name__ == "__main__":
    trn = loadtrnjson()
    round = int(sys.argv[1])
    trnfixed = fixtrn(trn, round)
    dumptrn(trnfixed, round)
    print('wrote json file for round', round)

