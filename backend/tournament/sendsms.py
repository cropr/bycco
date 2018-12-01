import simplejson as json

from django.core.management.base import BaseCommand, CommandError
from cd_subscription.models import FidePlayer, SmsRegistration
from cdp.models import CdTournament, CdSwarJson, CdSwarTournament
from cdp.swarconvert import pairingsfromswar
from cd_subscription import sms

class Command(BaseCommand):
    help = 'Fetch the standard_rating_list.zip from the site of the FIDE'

    pub = "Brought to you by Talistro the online membership platform for your club"

    def add_arguments(self, parser):
        parser.add_argument('trnshort', type=str)
        parser.add_argument('round', type=int)

    def handle(self, *args, **options):
        """
        sends sms to the registered
        :return: None
        """
        print('sending sms')

        trnshort = options.get('trnshort')
        round = options.get('round')

        try:
            trn = CdTournament.objects.get(shortname=trnshort)
        except CdTournament.DoesNotExist:
            print("tournament not found")
            return
        print('trn', trn.name)

        try:
            swartrn = CdSwarTournament.objects.get(tournament=trn)
        except CdSwarTournament.DoesNotExist:
            print("no matching swar tournament found")
            return
        print('swar trn', swartrn.swarname)

        try:
            swarjson = CdSwarJson.objects.get(tournament=swartrn, round=round,
                                              status='ACT')
        except CdSwarJson.DoesNotExist:
            print("no json file found for round")

        swjson = json.loads(swarjson.jsonfile)
        pairings = pairingsfromswar(swjson)
        smslist = []
        for ix,p in enumerate(pairings):
            if p["result"] == "Bye":
                smswhite = (
                    "{0} is Bye   {1}".format(p["white"],self.pub),
                    p["white_id"]
                )
                smslist.append(smswhite)
                continue
            if p["result"] == "--":
                continue
            smswhite = (
                "{0} plays on board {1} with white against {2}.   {3}".format(
                    p["white"], ix+1, p["black"], self.pub),
                p["white_id"]
            )
            smsblack = (
                "{0} plays on board {1} with black against {2}.   {3}".format(
                    p["black"], ix+1, p["white"], self.pub),
                p["black_id"]
            )
            smslist.append(smswhite)
            smslist.append(smsblack)
        sms.setup()
        for s in smslist:
            try:
                reg = SmsRegistration.objects.get(id_national=s[1])
            except SmsRegistration.DoesNotExist:
                continue
            sms.sendsms(s[0], reg.mobile)
            #print(s[0],reg.mobile)
