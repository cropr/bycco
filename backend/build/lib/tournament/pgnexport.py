# all rights reserved
# original copyright by Ruben Decrop
# modifications by Chessdevil Consulting BVBA

import simplejson as json
import os, os.path, shutil
import datetime

srcdir = os.path.join('data', 'pgnexport')
destdir = os.path.join('data', 'output')


def process_pgndir():
    for i in range(9):
        os.makedirs(os.path.join(destdir, 'R{0:d}'.format(i+1)), exist_ok=True)
    for (dirpath, dirnames, filenames) in os.walk(srcdir):
        if 'games.pgn' in filenames:
            dirchain, roundpath = os.path.split(dirpath)
            round = roundpath.split('-')[1]
            dirchain, catpath = os.path.split(dirchain)
            shutil.copyfile(
                os.path.join(dirpath, 'games.pgn'),
                os.path.join(destdir, 'R{0}'.format(round),
                             'BCYC2018-{0}-R{1}.pgn'.format(catpath, round)),
            )

if __name__ == "__main__":
    process_pgndir()
    print('wrote pgn to ', destdir)
