import datetime
import dbf
import io
import sys
import urllib.request
import zipfile

from django.core.management.base import BaseCommand, CommandError
from ...models import FidePlayer

class Command(BaseCommand):
    help = 'Fetch the standard_rating_list.zip from the site of the FIDE'

    def handle(self, *args, **options):
        """
        fetches the curretn fide list
        :return: None
        """
        print('fetching fide list')
        url = 'http://ratings.fide.com/download/players_list.zip'
        try:
            f = urllib.request.urlopen(url)
        except urllib.request.URLError:
            print('Cannot open url %s', url)
            sys.exit(1)
        fdata = f.read()
        f.close()
        fs1 = io.BytesIO(fdata)
        _zipfile_fide(fs1)
        print('done')


def _zipfile_fide(fs1):
    """
    reads the ratinglist zipfile, decrompress it and store all active
    players in the fideplayer collection
    :param fs1: filename (or file stream) of the zipfile
    :return: None
    """

    # read the zipfile in pldata and convert it to a byte stream
    print('decompressing  and zip file')
    zf = zipfile.ZipFile(fs1, mode='r')
    plist = zf.open(zf.namelist()[0]) # read first file in zipfile
    plist.readline()  # skip header line  # Read all the players

    # recreate the collection
    FidePlayer.objects.all().delete()
    i = 0
    dot = 0

    # read every dbase record
    for row in plist:
        line = row.decode('utf-8')
        p = FidePlayer()
        p.id_fide = line[0:15].strip()
        nfn = line[15:76].split(',')
        p.last_name = nfn[0].strip()
        p.first_name = nfn[1].strip() if len(nfn) == 2 else ''
        p.fidenation = line[76:79]
        p.gender = line[80]
        # p['birthdate'] = line[148:152]
        p.chesstitle = line[84:88].strip()
        p.fiderating = int(line[113:117].strip() or 0)
        i += 1
        dot += 1
        if dot == 1000:
            print('.',end='')
            sys.stdout.flush()
            dot = 0
        p.save()
    zf.close()
    print('\n{0:d} players created to fideplayer'.format(i))

