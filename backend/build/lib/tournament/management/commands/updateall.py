# Copyright Ruben Decrop


import logging
log = logging.getLogger(__name__)

import requests
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from tournament.models import Subscription

class Command(BaseCommand):
    help = 'Read the subscription2016.json and create emaillist'

    def handle(self, *args, **options):
        print('updating all participants from player.dbf')
        i = 0
        for s in Subscription.objects.all():
            i += 1
            idbel = s.idbel.lstrip('0')
            ca_url = "{0}ranking/bel/{1}".format(settings.CHESSAPI_URL, idbel)
            resp = requests.get(ca_url)
            if resp.status_code != 200:
                print('no record for idbel', idbel)
                continue
            bp = resp.json()
            s.ratingbel = bp.get('currentrating', 0)
            idfide = bp.get('idfide', '')
            fp = {}
            if idfide:
                ca_url = "{0}ranking/fide/{1}".format(settings.CHESSAPI_URL,
                                                     idfide)
                resp = requests.get(ca_url)
                if resp.status_code == 200:
                    fp = resp.json()
                    s.ratingfide = fp.get('currentrating', 0)
            s.rating = max(s.ratingfide, s.ratingbel)
            s.save()
        print('updated ratings of {0:d} subscriptions'.format(i))