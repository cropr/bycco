# Copyright Ruben Decrop

import logging
log = logging.getLogger(__name__)

import requests

from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import BaseRenderer, JSONRenderer

from .models import Subscription
from .serializers import SubscriptionSerializer

from .mail import sendconfirmationmail

class ImageRenderer(BaseRenderer):
    media_type = 'image/*'
    format = 'jpg'
    charset = None
    render_style = 'binary'

    def render(self, data, media_type=None, renderer_context=None):
        return data

@api_view(['GET'])
def test(request):
    return Response(data={'a':'b'})

@api_view(['POST'])
def subscription_confirmation(request, pk):

    try:
        subscription = Subscription.objects.get(pk=pk)
    except Subscription.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        subscription.confirmed = True
        subscription.save()
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
def subscriptions(request):

    # if request.method == 'GET':
    #     subscriptions = Subscription.objects.all()
    #     ss = SubscriptionSerializer(subscriptions, many=True)
    #     return Response(ss.data)

    if request.method == 'POST':

        ss = SubscriptionSerializer(data=request.data)
        if ss.is_valid():
            idbel = ss.validated_data.get('idbel')
            idbel = idbel.lstrip('0')
            ca_url = "{0}ranking/bel/{1}".format(settings.CHESSAPI_URL, idbel)
            resp = requests.get(ca_url)
            if resp.status_code != 200:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            bp = resp.json()
            idfide = bp.get('idfide', '')
            if idfide:
                ca_url = "{0}ranking/fide/{1}".format(settings.CHESSAPI_URL,
                                                     idfide)
                resp = requests.get(ca_url)
                fp = {}
                if resp.status_code == 200:
                    fp = resp.json()
            try:
                cs = Subscription.objects.get(idbel=idbel)
            except Subscription.DoesNotExist:
                cs = Subscription()
            cs.birthdate = bp.get('birthdate')
            cs.category = ss.validated_data.get('category')
            cs.chesstitle = bp.get('chesstitle')
            cs.emailparent = ss.validated_data.get('emailparent') or ''
            cs.emailplayer = ss.validated_data.get('emailplayer') or ''
            cs.federation = bp.get('federation')
            cs.nationalityfide = fp.get('nationalityfide', '')
            cs.first_name = bp.get('first_name')
            cs.fullnameattendant = ss.validated_data.get('fullnameattendant') or ''
            cs.fullnameparent = ss.validated_data.get('fullnameparent') or ''
            cs.gender = bp.get('gender')
            cs.idclub = bp.idclub
            cs.idfide = idfide
            cs.idbel = idbel
            cs.last_name = bp.get('last_name')
            cs.locale = request.LANGUAGE_CODE.lower()[:2]
            cs.mobileattendant = ss.validated_data.get('mobileattendant') or ''
            cs.mobileparent = ss.validated_data.get('mobileparent') or ''
            cs.mobileplayer = ss.validated_data.get('mobileplayer') or ''
            cs.ratingbel = bp.get('currentrating')
            cs.ratingfide = fp.get('currentrating', 0)
            cs.rating = max(cs.natrating, cs.fiderating)
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
            cs.paymessage = "+++020/170{0:01d}/{1:03d}{2:02d}+++".format(
                rm1, rm2, rm3)
            cs.save()
            return Response({'id': cs.id, 'paymessage': cs.paymessage},
                status=status.HTTP_201_CREATED)
        return Response(ss.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@renderer_classes((ImageRenderer, JSONRenderer))
def subscription_photo(request, pk):

    pass

    # try:
    #     subscription = Subscription.objects.get(pk=pk)
    # except Subscription.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)
    #
    # if request.method == 'GET':
    #     return Response(content_type=subscription.badgemimetype,
    #                     data=subscription.badgeimage)
    #
    # if request.method == 'POST':
    #     ps = PhotoSerializer(data=request.data)
    #     if ps.is_valid():
    #         try:
    #             header, data = ps.validated_data.get('imagedata').split(',')
    #             subscription.badgemimetype = header.split(':')[1].split(';')[0]
    #             subscription.badgeimage = a2b_base64(data)
    #             subscription.badgelength = len(subscription.badgeimage)
    #             subscription.save()
    #             return Response(status=status.HTTP_201_CREATED)
    #         except Exception as e:
    #             return Response(status=status.HTTP_400_BAD_REQUEST)

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

@api_view(['GET'])
def participants(request, cat):

    pass

    # players = Subscription.objects.filter(category=cat).order_by('-rating')
    # data = [{
    #     'id': p.id,
    #     'category': p.category,
    #     'name': p.name,
    #     'firstname': p.firstname,
    #     'rating': p.rating,
    #     'id_club': p.id_club,
    #     'fidenation': p.fidenation,
    #     'confirmed': p.confirmed,
    # } for p in players]
    # return Response(data)

@api_view(['GET', 'POST'])
def mgmtattendees(request):

    pass

    # if request.method == 'GET':
    #     param = request.GET
    #     start = to_int(param.get('start'), 0)
    #     count = to_int(param.get('count'), 40)
    #     query = Subscription.objects.all()
    #     cat = param.get('cat')
    #     if cat:
    #         query = query.filter(category=cat)
    #     ss = param.get('ss')
    #     if ss:
    #         query = query.filter(name__icontains=ss)
    #     n_attendees = query.count()
    #     query = query.order_by('name')[start:start+count]
    #     result = {
    #         'ss': ss,
    #         'cat': cat,
    #         'start': start,
    #         'count': count,
    #         'n_attendees': n_attendees,
    #         'attendees': [{
    #                 'id': p.id,
    #                 'category': p.category,
    #                 'name': p.name,
    #                 'firstname': p.firstname,
    #                 'rating': p.rating,
    #                 'id_national': p.id_national,
    #                 'id_club': p.id_club,
    #                 'fidenation': p.fidenation,
    #                 'confirmed': p.confirmed,
    #                 'meals': p.custom1,
    #                 'present': p.custom2,
    #                 'payamount': p.payamount,
    #             } for p in query]
    #     }
    #     return Response(result)
    #
    # if request.method == 'POST':
    #     ss = request.data
    #     try:
    #         cs = Subscription()
    #         cs.category = ss.get('category')
    #         cs.chesstitle = ss.get('chesstitle')
    #         cs.firstname = ss.get('firstname')
    #         cs.gender = ss.get('gender')
    #         cs.id_national = '0'
    #         cs.locale = request.LANGUAGE_CODE.lower()[:2]
    #         cs.name = ss.get('name')
    #         cs.custom1 = ss.get('meals')
    #         cs.custom2 = ss.get('present')
    #         cs.save()
    #         cs.id_national = str(int(cs.pk) + 100000)
    #         cs.save()
    #         return Response(dict(id_national=cs.id_national),
    #                         status=status.HTTP_201_CREATED)
    #     except Exception as e:
    #         return Response(e, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def mgmtattendee_detail(request, id):

    pass

    # try:
    #     p = Subscription.objects.get(id_national=id)
    # except Subscription.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)
    #
    # if request.method == 'GET':
    #     attendee = {
    #         'id': p.id,
    #         'category': p.category,
    #         'name': p.name,
    #         'firstname': p.firstname,
    #         'gender': p.gender,
    #         'rating': p.rating,
    #         'id_national': p.id_national,
    #         'id_club': p.id_club,
    #         'fidenation': p.fidenation,
    #         'confirmed': p.confirmed,
    #         'meals': p.custom1,
    #         'present': p.custom2,
    #         'payamount': p.payamount,
    #     }
    #     return Response(dict(attendee=attendee))
    #
    # if request.method == 'PUT':
    #     data = request.data
    #     p.name = data.get('name')
    #     p.firstname = data.get('firstname')
    #     p.chesstitle = data.get('chesstitle','')
    #     p.category = data.get('category')
    #     p.custom1 = data.get('meals')
    #     p.custom2 = data.get('present')
    #     p.gender = data.get('gender')
    #     p.payamount = int(data.get('payamount', 0))
    #     try:
    #         p.save()
    #         return Response(dict(id_national=p.id_national),
    #                         status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response(e, status=status.HTTP_406_NOT_ACCEPTABLE)
    #
    # if request.method == 'DELETE':
    #     try:
    #         p.delete()
    #         return Response(status=status.HTTP_204_NO_CONTENT)
    #     except Exception as e:
    #         return Response(e, status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['GET', 'POST'])
def mgmtattendee_photo(request, id):

    pass

    # p = None
    # try:
    #     p = Subscription.objects.get(id_national=id)
    #     foundplayer = True
    # except Subscription.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)
    #
    # if request.method == 'GET':
    #     if not p or not p.badgelength:
    #         with open('../cd_subscription/static/img/nobody.png', 'rb') as img:
    #             return HttpResponse(img.read(), content_type="image/png")
    #     return HttpResponse(p.badgeimage, content_type=p.badgemimetype)
    #
    # if request.method == 'POST':
    #     data=request.data
    #     try:
    #         header, data = data.get('imagedata').split(',')
    #         p.badgemimetype = header.split(':')[1].split(';')[0]
    #         p.badgeimage = a2b_base64(data)
    #         p.badgelength = len(p.badgeimage)
    #         p.save()
    #         return Response(status=status.HTTP_201_CREATED)
    #     except Exception as e:
    #         return Response(e, status=status.HTTP_400_BAD_REQUEST)
