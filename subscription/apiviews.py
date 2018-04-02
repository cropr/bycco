# Copyright Ruben Decrop

import logging
log = logging.getLogger(__name__)

import requests
import iso8601
from binascii import a2b_base64
from django.shortcuts import redirect
from django.conf import settings
from django.http.response import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import BaseRenderer, JSONRenderer

from .models import (
    CdSwarTournament,
    CdSwarJson,
    CdTournament,
    CdTournamentPrizes,
    Subscription
)

from .serializers import (
    SubscriptionSerializer,
    SwarTournamentSerializer,
    SwarJsonSerializer,
    SwarJsonSerializerSmall,
    TournamentSerializer,
)

from .swarconvert import (
    pairingsfromswar,
    standingsfromswar,
    playercardfromswar,
    prizesfromswar,
)

from .mail import sendconfirmationmail

def to_int(s, default):
    """
    convert s to integer , returning default if failing
    :param s: str
    :param default: int
    :return: an int
    """
    try:
        return int(s)
    except:
        return default

class ImageRenderer(BaseRenderer):
    media_type = 'image/*'
    format = 'jpg'
    charset = None
    render_style = 'binary'

    def render(self, data, media_type=None, renderer_context=None):
        return data

# subscription

@api_view(['POST'])
def subscription_confirmation(request, idsub):

    try:
        subscription = Subscription.objects.get(pk=idsub)
    except Subscription.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        subscription.confirmed = True
        subscription.save()
        sendconfirmationmail(subscription)
        return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def subscription_resend(request, idsub):
    """ resend confirmation email"""

    try:
        subscription = Subscription.objects.get(pk=idsub)
    except Subscription.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        subscription.confirmed = True
        sendconfirmationmail(subscription)
        return Response(status=status.HTTP_200_OK)

@api_view(['GET', 'PUT', 'DELETE'])
def subscription_detail(request, pk):

    try:
        cs = Subscription.objects.get(pk=pk)
    except Subscription.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        ss = SubscriptionSerializer(data=request.data)
        return Response(ss.data)

    if request.method == 'PUT':
        ss = SubscriptionSerializer(data=request.data)
        if ss.is_valid():
            cs.category = ss.validated_data.get('category')
            cs.emailparent = ss.validated_data.get('emailparent') or ''
            cs.emailplayer = ss.validated_data.get('emailplayer') or ''
            cs.fullnameattendant = ss.validated_data.get('fullnameattendant') or ''
            cs.fullnameparent = ss.validated_data.get('fullnameparent') or ''
            cs.mobileattendant = ss.validated_data.get('mobileattendant') or ''
            cs.mobileparent = ss.validated_data.get('mobileparent') or ''
            cs.mobileplayer = ss.validated_data.get('mobileplayer') or ''
            cs.save()
            return Response({'id': cs.id, 'paymessage': cs.paymessage},
                status=status.HTTP_200_OK)
            return Response(ss.data)
        return Response(ss.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        cs.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST', 'GET'])
def subscription_all(request):

    # if request.method == 'GET':
    #     subscriptions = Subscription.objects.all()
    #     ss = SubscriptionSerializer(subscriptions, many=True)
    #     return Response(ss.data)

    if request.method == 'POST':

        ss = SubscriptionSerializer(data=request.data.get('subscription'))
        if ss.is_valid():
            idbel = ss.validated_data.get('idbel')
            idbel = idbel.lstrip('0')
            ca_url = "{0}ranking/bel/{1}".format(settings.CHESSAPI_URL, idbel)
            resp = requests.get(ca_url)
            if resp.status_code != 200:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            bp = resp.json()
            idfide = bp.get('idfide', '')
            fp = {}
            if idfide:
                ca_url = "{0}ranking/fide/{1}".format(settings.CHESSAPI_URL,
                                                     idfide)
                resp = requests.get(ca_url)
                if resp.status_code == 200:
                    fp = resp.json()
            try:
                cs = Subscription.objects.get(idbel=idbel)
            except Subscription.DoesNotExist:
                cs = Subscription()
            cs.birthdate = bp.get('birthdate').split('T')[0]
            cs.category = ss.validated_data.get('category')
            cs.chesstitle = bp.get('chesstitle') or ''
            cs.emailparent = ss.validated_data.get('emailparent') or ''
            cs.emailplayer = ss.validated_data.get('emailplayer') or ''
            cs.federation = bp.get('federation')
            cs.nationalityfide = fp.get('nationalityfide', '')
            cs.first_name = bp.get('first_name')
            cs.fullnameattendant = ss.validated_data.get('fullnameattendant') or ''
            cs.fullnameparent = ss.validated_data.get('fullnameparent') or ''
            cs.gender = bp.get('gender')
            cs.idclub = bp.get('idclub')
            cs.idfide = idfide
            cs.idbel = idbel
            cs.last_name = bp.get('last_name')
            cs.locale = request.LANGUAGE_CODE.lower()[:2]
            cs.mobileattendant = ss.validated_data.get('mobileattendant') or ''
            cs.mobileparent = ss.validated_data.get('mobileparent') or ''
            cs.mobileplayer = ss.validated_data.get('mobileplayer') or ''
            cs.ratingbel = bp.get('currentrating')
            cs.ratingfide = fp.get('currentrating', 0)
            cs.rating = max(cs.ratingbel, cs.ratingfide)
            cs.nationalitybel = bp.get('nationalitybel')
            cs.payamount = 0
            try:
                cs.save()
            except Exception as e:
                log.exception('Saving to db')
            nr = 201800000 + cs.pk
            rm1 = cs.pk // 1000
            rm2 = cs.pk % 1000
            rm3 = nr % 97 or 97
            cs.paymessage = "+++020/180{0:01d}/{1:03d}{2:02d}+++".format(
                rm1, rm2, rm3)
            cs.save()
            return Response({'id': cs.id, 'paymessage': cs.paymessage},
                status=status.HTTP_201_CREATED)
        return Response(ss.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@renderer_classes((ImageRenderer, JSONRenderer))
def subscription_photo(request, idsub):

    pass

    try:
        subscription = Subscription.objects.get(pk=idsub)
    except Subscription.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(content_type=subscription.badgemimetype,
                        data=subscription.badgeimage)

    if request.method == 'POST':
        photo = request.data.get('photo')
        if photo:
            try:
                header, data = photo.split(',')
                subscription.badgemimetype = header.split(':')[1].split(';')[0]
                subscription.badgeimage = a2b_base64(data)
                subscription.badgelength = len(subscription.badgeimage)
                subscription.save()
                return Response(status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(status=status.HTTP_400_BAD_REQUEST)

# chess player

@api_view(['GET'])
def belplayer(request, idbel):

    """fetch belgian rating details"""

    idbel = idbel.lstrip('0')
    ca_url = "{0}ranking/bel/{1}".format(settings.CHESSAPI_URL, idbel)
    resp = requests.get(ca_url)
    details = {}
    if resp.status_code == 200:
        details.update(resp.json())
        details['idbel'] = details['_id']
        try:
            cs = Subscription.objects.get(idbel=idbel)
            if cs.confirmed:
                details['alreadysubscribed'] = True
        except:
            pass
        return Response(details)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def fideplayer(request, idfide):

    idfide = idfide.lstrip('0')
    ca_url = "{0}ranking/fide/{1}".format(settings.CHESSAPI_URL, idfide)
    resp = requests.get(ca_url)
    details = {}
    if resp.status_code == 200:
        details.update(resp.json())
        details['idfide'] = details['_id']
        return Response(details)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

# ateendees
@api_view(['GET', 'POST'])
def attendee_all(request):

    if request.method == 'GET':
        param = request.GET
        start = to_int(param.get('start'), 0)
        count = to_int(param.get('count'), 40)
        ss = param.get('ss')
        query = Subscription.objects.all()
        cat = param.get('cat')
        if cat:
            if ',' in cat:
                cats = cat.split(',')
                query = query.filter(category__in=cats)
            else:
                query = query.filter(category=cat)
        ss = param.get('ss')
        if ss:
            query = query.filter(last_name__icontains=ss)
        n_attendees = query.count()
        query = query.order_by('last_name')[start:start+count]
        result = {
            'ss': ss,
            'cat': cat,
            'start': start,
            'count': count,
            'n_attendees': n_attendees,
            'attendees': [{
                    'id': p.id,
                    'category': p.category,
                    'last_name': p.last_name,
                    'first_name': p.first_name,
                    'rating': p.rating,
                    'idbel': p.idbel,
                    'idclub': p.idclub,
                    'nationalityfide': p.nationalityfide,
                    'confirmed': p.confirmed,
                    'meals': p.custom1,
                    'present': p.present.isoformat() if p.present else '',
                    'payamount': p.payamount,
                } for p in query]
        }
        log.info('result: %s', result)
        return Response(result)

    if request.method == 'POST':
        ss = request.data
        try:
            cs = Subscription()
            cs.category = ss.get('category')
            cs.chesstitle = ss.get('chesstitle')
            cs.first_name = ss.get('first_name')
            cs.gender = ss.get('gender')
            cs.id_national = '0'
            cs.locale = request.LANGUAGE_CODE.lower()[:2]
            cs.last_name = ss.get('last_name')
            cs.custom1 = ss.get('meals')
            cs.custom2 = ss.get('present')
            cs.save()
            cs.id_national = str(int(cs.pk) + 100000)
            cs.save()
            return Response(dict(id_national=cs.id_national),
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def attendee_detail(request, id):

    try:
        p = Subscription.objects.get(id=id)
    except Subscription.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        attendee = {
            'id': p.id,
            'birthdate': p.birthdate.isoformat() if p.birthdate else '',
            'category': p.category,
            'chesstitle': p.chesstitle,
            'confirmed': p.confirmed,
            'emailparent': p.emailparent,
            'emailplayer': p.emailparent,
            'federation': p.federation,
            'first_name': p.first_name,
            'fullnameattendant': p.fullnameattendant,
            'fullnameparent': p.fullnameparent,
            'gender': p.gender,
            'idclub': p.idclub,
            'idbel': p.idbel,
            'idfide': p.idfide,
            'last_name': p.last_name,
            'locale': p.locale,
            'meals': p.custom1,
            'mobileattendant': p.mobileattendant,
            'mobileparent': p.mobileparent,
            'mobileplayer': p.mobileplayer,
            'nationalitybel': p.nationalitybel,
            'nationalityfide': p.nationalityfide,
            'payamount': p.payamount,
            'paydate': p.paydate.isoformat() if p.paydate else '',
            'paymessage': p.paymessage,
            'present': p.present.isoformat() if p.present else '',
            'rating': p.rating,
            'ratingbel': p.ratingbel,
            'ratingfide': p.ratingfide,
            'remarks': p.remarks,
        }
        return Response(dict(attendee=attendee))

    if request.method == 'PUT':
        data = request.data.get('attendee', {})
        # p.birthdate = data.get('last_name')
        p.category = data.get('category')
        p.chesstitle = data.get('chesstitle','')
        p.emailparent = data.get('emailparent', '')
        p.emailplayer = data.get('emailplayer', '')
        p.first_name = data.get('first_name')
        if data.get('fullnameattendant'):
            p.fullnameattendant = data.get('fullnameattendant')
        if data.get('fullnameparent'):
            p.fullnameparent = data.get('fullnameparent')
        p.last_name = data.get('last_name')
        if data.get('locale'):
            p.locale = data.get('locale')
        p.meals = data.get('custom1')
        if data.get('mobileattendant'):
            p.mobileattendant = data.get('mobileattendant')
        if data.get('mobilemobileparent'):
            p.mobileparent = data.get('mobileparent')
        if data.get('mobileplayer'):
            p.mobileplayer = data.get('mobileplayer')
        p.nationalityfide = data.get('nationalityfide')
        p.payamount = int(data.get('payamount', 0))
        # p.paydate = data.get('paydate')
        if 'present' in data:
            present = data.get('present')
            if present:
                p.present = iso8601.parse_date(present)
            else:
                p.present = None
        p.rating = data.get('rating')
        if data.get('ratingbel'):
            p.ratingbel = data.get('ratingbel')
        if data.get('ratingfide'):
            p.ratingfide = data.get('ratingfide')
        if data.get('remarks'):
            p.remarks = data.get('remarks')
        if data.get('custom1'):
            p.custom1 = data.get('meals')
        try:
            p.save()
            return Response(dict(id=p.id),
                            status=status.HTTP_200_OK)
        except Exception as e:
            log.exception("could not update attendee")
            return Response(e, status=status.HTTP_406_NOT_ACCEPTABLE)

    if request.method == 'DELETE':
        try:
            p.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(e, status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['GET', 'POST'])
@renderer_classes((ImageRenderer, JSONRenderer))
def attendee_photo(request, id):

    p = None
    try:
        p = Subscription.objects.get(id=id)
        foundplayer = True
    except Subscription.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        if not p or not p.badgelength:
            return redirect('/static/img/nobody.png')
        return Response(data=p.badgeimage, content_type=p.badgemimetype)

    if request.method == 'POST':
        data=request.data
        try:
            header, data = data.get('imagedata').split(',')
            p.badgemimetype = header.split(':')[1].split(';')[0]
            p.badgeimage = a2b_base64(data)
            p.badgelength = len(p.badgeimage)
            p.save()
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

# tournament
@api_view(['GET', 'POST'])
def tournament_all(request):

    if request.method == 'POST':
        trn_serializer = TournamentSerializer(data=request.data)
        if trn_serializer.is_valid():
            trn_serializer.save()
            return Response(trn_serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        shortname = request.GET.get('shortname', None)
        trns = CdTournament.objects.all()
        if shortname:
            trns = trns.filter(shortname=shortname)
        trn_serializer = TournamentSerializer(trns, many=True)
        return Response(dict(trns=trn_serializer.data))

@api_view(['GET', 'DELETE'])
def tournament_one(request, id_trn):
    try:
        trn = CdSwarTournament.objects.get(id=id_trn)
    except CdSwarTournament.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        trn_serializer = SwarTournamentSerializer(trn)
        return Response(trn_serializer.data)

    if request.method == 'DELETE':
        trn.delete()
        trns = CdSwarTournament.objects.all()
        trn_serializer = SwarTournamentSerializer(trns, many=True)
        return Response(trn_serializer.data)

@api_view(['GET'])
def tournament_pairings(request, id_trn, round):
    try:
        trn = CdTournament.objects.get(id=id_trn)
    except CdTournament.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    swarround = int(round) + 1
    try:
        swartrn = CdSwarTournament.objects.get(tournament=trn)
    except CdSwarTournament.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    try:
        swarjson = CdSwarJson.objects.get(tournament=swartrn, round=swarround,
                                      status='ACT')
    except CdSwarJson.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    trndata = json.loads(swarjson.jsonfile)
    data = {
        'id_trn': trn.id,
        'tournament': trn.name,
        'round': int(round),
        'pairings': pairingsfromswar(trndata)
    }
    return Response(data)

@api_view(['GET'])
def tournament_standings(request, id_trn, round):
    try:
        trn = CdTournament.objects.get(id=id_trn)
    except CdTournament.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    swarround = int(round) + 1
    try:
        swartrn = CdSwarTournament.objects.get(tournament=trn)
    except CdSwarTournament.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    try:
        swarjson = CdSwarJson.objects.get(tournament=swartrn, round=swarround,
                                      status='ACT')
    except CdSwarJson.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    trndata = json.loads(swarjson.jsonfile)
    data = {
        'id_trn': trn.id,
        'tournament': trn.name,
        'round': int(round),
        'standings': standingsfromswar(trndata)
    }
    return Response(data)

@api_view(['GET'])
def tournament_playercard(request, id_trn, id_player):
    try:
        id_player = int(id_player)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    try:
        trn = CdTournament.objects.get(id=id_trn)
    except CdTournament.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    try:
        swartrn = CdSwarTournament.objects.get(tournament=trn)
    except CdSwarTournament.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    swarjsons = CdSwarJson.objects.filter(tournament=swartrn, status='ACT')
    topround = swarjsons.aggregate(topround=Max('round')).get('topround', 1)
    try:
        swarjson = CdSwarJson.objects.get(tournament=swartrn, round=topround,
            status='ACT')
    except CdSwarJson.DoesNotExist:
        log.debug("swarjson for topround %d not found", topround)
        return Response(status=status.HTTP_404_NOT_FOUND)
    trndata = json.loads(swarjson.jsonfile)
    return Response(playercardfromswar(trndata, id_player))

@api_view(['GET', 'POST'])
def tournament_prizes(request, id_trn):
    try:
        trn = CdTournament.objects.get(id=id_trn)
    except CdTournament.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        cat = trn.shortname
        try:
            swartrn = CdSwarTournament.objects.get(tournament=trn)
        except CdSwarTournament.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        swarjsons = CdSwarJson.objects.filter(tournament=swartrn, status='ACT')
        topround = swarjsons.aggregate(topround=Max('round')).get('topround', 1)
        try:
            swarjson = CdSwarJson.objects.get(tournament=swartrn, round=topround,
                status='ACT')
        except CdSwarJson.DoesNotExist:
            log.debug("swarjson for topround %d not found", topround)
            return Response(status=status.HTTP_404_NOT_FOUND)
        trndata = json.loads(swarjson.jsonfile)
        prizesjson = json.dumps(prizesfromswar(trndata, cat))
        if not hasattr(trn, 'cdtournamentprizes'):
            trnprizes = CdTournamentPrizes(tournament=trn)
            trnprizes.jsonprizes = prizesjson
            trnprizes.save()
        else:
            trnprizes = trn.cdtournamentprizes
            trnprizes.jsonprizes = prizesjson
            trnprizes.save()
        return Response(json.loads(prizesjson))

    if request.method == 'GET':
        if hasattr(trn, 'cdtournamentprizes'):
            return Response(json.loads(trn.cdtournamentprizes.jsonprizes))
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def tournament_swar(request, id_trn):
    """
    enable swar on a tournament
    """
    try:
        trn = CdTournament.objects.get(id=id_trn)
    except CdTournament.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        swartrn_serializer = SwarTournamentSerializer(data=request.data)
        if swartrn_serializer.is_valid():
            swartrn = swartrn_serializer.save(tournament=trn)
            swardata = SwarTournamentSerializer(swartrn).data
            swardata.update(TournamentSerializer(trn).data)
            return Response(swardata)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def swartrn_all(request):
    swardata = {}
    for swartrn in CdSwarTournament.objects.all():
        srl = SwarTournamentSerializer(swartrn)
        swardata[swartrn.tournament_id] = srl.data
    for trn in CdTournament.objects.all():
        if trn.id in swardata:
            swardata[trn.id].update(TournamentSerializer(trn).data)
    return Response(swardata.values())

@api_view(['GET', 'DELETE'])
def swartrn_one(request, id_trn):
    try:
        trn = CdSwarTournament.objects.get(tournament_id=id_trn)
    except CdSwarTournament.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        trn_serializer = SwarTournamentSerializer(trn)
        return Response(trn_serializer.data)

    if request.method == 'DELETE':
        trn.delete()
        trns = CdSwarTournament.objects.all()
        trn_serializer = SwarTournamentSerializer(trns, many=True)
        return Response(trn_serializer.data)

@api_view(['POST'])
def swarfile_publication(request, id_trn, id_swar):
    try:
        trn = CdSwarTournament.objects.get(tournament_id=id_trn)
    except CdSwarTournament.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    try:
        swar = CdSwarJson.objects.get(id=id_swar)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    CdSwarJson.objects.filter(tournament=id_trn, status='ACT',
                              round=swar.round).update(status='OUT')
    CdSwarJson.objects.filter(tournament=id_trn, id=id_swar).update(status='ACT')
    # TODO create a optimized publishing JSON string
    swarjsons = CdSwarJson.objects.filter(tournament=id_trn).order_by(
        '-round', '-uploaddate')
    ss = SwarJsonSerializerSmall(swarjsons, many=True)
    return Response(ss.data)

@api_view(['GET', 'POST'])
def swarfile_all(request, id_trn):

    try:
        trn = CdSwarTournament.objects.get(tournament_id=id_trn)
    except CdSwarTournament.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        # add a new Swar file
        data = request.data
        data['tournament'] = id_trn
        swar_serializer  = SwarJsonSerializer(data=data)
        if swar_serializer.is_valid():
            swar_serializer.save()
            trn.swarname = swar_serializer.data['name']
            trn.save()
            swarjsons = CdSwarJson.objects.filter(tournament=id_trn).order_by(
                '-round', '-uploaddate')
            ss = SwarJsonSerializerSmall(swarjsons, many=True)
            return Response(ss.data)
        else:
            log.debug('invalid data %s', swar_serializer.data)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        # get all swarupload files
        swarjsons = CdSwarJson.objects.filter(tournament=id_trn).order_by(
                '-round', '-uploaddate')
        ss = SwarJsonSerializerSmall(swarjsons, many=True)
        return Response(ss.data)

@api_view(['GET', 'DELETE'])
def swarfile_one(request, id_trn, id_swar):

    try:
        swar = CdSwarJson.objects.get(tournament=id_trn, id=id_swar)
    except CdSwarJson.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        ss = SwarJsonSerializer(swar)
        return Response(ss.data)

    if request.method == 'DELETE':
        swar.delete()
        swarjsons = CdSwarJson.objects.filter(tournament=id_trn).order_by(
                '-round', '-uploaddate')
        ss = SwarJsonSerializerSmall(swarjsons, many=True)
        return Response(ss.data)

@api_view(['GET'])
def topround(request, id_trn):
    try:
        trn = CdTournament.objects.get(id=id_trn)
    except CdTournament.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    try:
        swartrn = CdSwarTournament.objects.get(tournament=trn)
    except CdSwarTournament.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    swarjsons = CdSwarJson.objects.filter(tournament=swartrn)
    topround = swarjsons.aggregate(topround=Max('round')).get('topround', 1) - 1
    return Response(topround)
