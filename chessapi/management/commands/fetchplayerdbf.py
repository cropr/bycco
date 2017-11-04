import datetime
import dbf
import io
import sys
import urllib.request
import zipfile

from django.core.management.base import BaseCommand, CommandError
from ...models import BelPlayer

class Command(BaseCommand):
    help = 'Fetch the player.dbf from the site of the KBSB'

    def handle(self, *args, **options):
        print('fetching player.dbf')
        now = datetime.datetime.now()
        year = now.year
        month = (now.month - 1) // 3 * 3 + 1
        print('period {0:4d}-{1:02d}'.format(year, month))
        url = 'http://www.frbe-kbsb.be/sites/manager/ELO/' \
              'PLAYER_{0:4d}{1:02d}.ZIP'.format(year, month)
        try:
            f = urllib.request.urlopen(url)
        except urllib.request.URLError:
            print('Cannot open url %s', url)
            sys.exit(1)
        fdata = f.read()
        f.close()
        fs1 = io.BytesIO(fdata)
        _zipfile_bel(fs1)
        print('done')

beltitle = {
    '': '', 'WCM': 'WCM', 'WF': 'WFM', 'CM': 'CM', 'FM': 'FM', 'WI': 'WIM',
    'WGM': 6, 'IM': 'IM', 'GM': 'GM'
}


def _zipfile_bel(fs1):
    """
    reads the ratinglist zipfile, decrompress it and store all active
    players in the belplayer collection
    :param fs1: filename (or file stream) of the zipfile
    :return: None
    """

    # read the zipfile in pldata and convert it to a byte stream
    zf = zipfile.ZipFile(fs1, mode='r')
    zfd = zf.open(zf.namelist()[0]) # read first file in zipfile
    pldata = zfd.read()
    zfd.close()
    plbindata = io.BytesIO(pldata)

    # create a dbf file from the byte stream
    players = dbf.Dbf()
    players.openOn(plbindata)
    print('player.dbf contains {0:d} records'.format(len(players)))

    # empty the table
    BelPlayer.objects.all().delete()
    i=0
    dot = 0

    # read every dbase record
    for row in range(len(players)):
        try:
            line = players[row]
        except:
            print('dbf read error for line %d', row)
            sys.exit(1)
        if line["SUPPRESS"]:
            continue
        p = BelPlayer()
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
            year, month,day = (1900,1,1)
        p.birthdate = datetime.date(year, month, day)
        p.id_national = str(line['MATRICULE'])
        p.id_club = str(line['CLUB'])
        p.chesstitle = beltitle[line['TITRE']] if line['TITRE'] in \
                                                     beltitle else ''
        p.id_fide = str(line['FIDE'])
        p.natrating = line['ELO_CALCUL']
        p.federation = line['FEDERATION']
        p.nationality = line['NOUV_MOD']
        i += 1
        dot += 1
        if dot == 100:
            print(',', end='')
            sys.stdout.flush()
            dot = 0
        p.save()
    print('\n{0:d} players created to belplayer'.format(i))