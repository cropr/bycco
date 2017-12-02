# Copyright Ruben Decrop

import simplejson
from ...models import BelPlayer, FidePlayer

import logging
log = logging.getLogger(__name__)

from django.core.management.base import BaseCommand, CommandError
from ...models import BelPlayer, FidePlayer, Subscription

class Command(BaseCommand):
    help = 'Read the subscription2016.json and create emaillist'

    def handle(self, *args, **options):
        print('updating all participants from player.dbf')
        for s in Subscription.objects.all():
            idn = s.id_national
            bs = BelPlayer.objects.get(id_national=idn)
            gender = bs.gender
            if s.gender != gender:
                s.gender = gender
                if gender == 'M':
                    s.category = 'B' + s.category[1:]
                else:
                    s.category = 'G' + s.category[1:]
            s.natrating = bs.natrating or 0
            fiderating = 0
            if bs.id_fide and bs.id_fide != '0':
                s.id_fide = bs.id_fide
                try:
                    fs = FidePlayer.objects.get(id_fide=s.id_fide)
                    fiderating = fs.fiderating or 0
                except FidePlayer.DoesNotExist:
                    log.info('No fide record for id_fide: %s', s.id_fide)
                s.fiderating = fiderating
            s.rating = max(s.natrating, s.fiderating)
            s.save()
        print('done')