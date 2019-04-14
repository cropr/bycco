# Copyright Ruben Decrop


import logging
log = logging.getLogger(__name__)

import requests
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from tournament.models import CdTournament, CdSwarTournament, CdSwarJson

class Command(BaseCommand):
    help = 'Copy last round of round robin to current round'

    def add_arguments(self, parser):
        parser.add_argument('shortname', nargs='+', type=str)
        parser.add_argument('round', nargs='+', type=int)

    def handle(self, *args, **options):
        shortname = options['shortname'][0]
        round = options['round'][0]
        print('fixing round robin:', shortname, round)
        try:
            trn = CdTournament.objects.get(shortname=shortname)
        except CdTournament.DoesNotExist:
            print('Could not find tournament')
            return 
        print('Found tournament', trn.name)
        try:
            swartrn = CdSwarTournament.objects.get(tournament=trn)
        except CdSwarTournament.DoesNotExist:
            print('Could not find swar tournament')
            return
        try:
            maxjson = CdSwarJson.objects.get(swartrn=swartrn, round=9)
        except CdSwarJson.DoesNotExist:
            print('Could not find swar json file round 9')
            return 
        try:
            currjson = CdSwarJson.objects.get(swartrn=swartrn, round=round)
            currjson.jsonfile = maxjson.jsonfile
        except CdSwarJson.DoesNotExist:
            print('Create JSON file round', round)
            currjson = CdSwarJson(round=round, jsonfile=maxjson.jsonfile, 
                swartrn=swartrn)
        currjson.save()
        print('round fixed')
        