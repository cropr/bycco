# Copyright Ruben Decrop

import logging
log = logging.getLogger(__name__)

from django.http import HttpResponse
from binascii  import a2b_base64
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import BaseRenderer, JSONRenderer
from bycco.util import to_int

from .models import BelPlayer, FidePlayer, CdSubscription, SmsRegistration

from .serializers import (
    SubscriptionSerializer,
    BelplayerSerializer,
    FideplayerSerializer,
    PhotoSerializer,
)
from .mail import sendconfirmationmail

class ImageRenderer(BaseRenderer):
    media_type = 'image/*'
    format = 'jpg'
    charset = None
    render_style = 'binary'

    def render(self, data, media_type=None, renderer_context=None):
        return data

@api_view(['POST'])
def subscription_confirmation(request, pk):

    try:
        subscription = CdSubscription.objects.get(pk=pk)
    except CdSubscription.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        subscription.confirmed = True
        subscription.save()
        sendconfirmationmail(subscription)
        return Response(status=status.HTTP_200_OK)

@api_view(['GET', 'PUT', 'DELETE'])
def subscription_detail(request, pk):

    try:
        cs = CdSubscription.objects.get(pk=pk)
    except CdSubscription.DoesNotExist:
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
def subscription_list(request):

    pass

    if request.method == 'GET':
        subscriptions = CdSubscription.objects.all()
        ss = SubscriptionSerializer(subscriptions, many=True)
        return Response(ss.data)

    if request.method == 'POST':

        ss = SubscriptionSerializer(data=request.data)
        if ss.is_valid():
            id_national = ss.validated_data.get('id_national')
            try:
                bp = BelPlayer.objects.get(id_national=id_national)
            except BelPlayer.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if bp.id_fide:
                try:
                    fp = FidePlayer.objects.get(id_fide=bp.id_fide)
                except:
                    fp = None
            try:
                cs = CdSubscription.objects.get(id_national=id_national)
            except CdSubscription.DoesNotExist:
                cs = CdSubscription()
            cs.birthdate = bp.birthdate
            cs.category = ss.validated_data.get('category')
            cs.chesstitle = bp.chesstitle
            cs.emailparent = ss.validated_data.get('emailparent') or ''
            cs.emailplayer = ss.validated_data.get('emailplayer') or ''
            cs.federation = bp.federation
            cs.fidenation = fp.fidenation if fp else ''
            cs.fiderating = fp.fiderating if fp else 0
            cs.firstname = bp.firstname
            cs.fullnameattendant = ss.validated_data.get('fullnameattendant') or ''
            cs.fullnameparent = ss.validated_data.get('fullnameparent') or ''
            cs.gender = bp.gender
            cs.id_club = bp.id_club
            cs.id_fide = bp.id_fide or ''
            cs.id_national = bp.id_national
            cs.locale = request.LANGUAGE_CODE.lower()[:2]
            cs.mobileattendant = ss.validated_data.get('mobileattendant') or ''
            cs.mobileparent = ss.validated_data.get('mobileparent') or ''
            cs.mobileplayer = ss.validated_data.get('mobileplayer') or ''
            cs.name = bp.name
            cs.natrating = bp.natrating
            cs.nationality = bp.nationality
            cs.payamount = 0
            cs.rating = max(cs.natrating, cs.fiderating)
            try:
                cs.save()
            except Exception as e:
                log.exception('Saving to db')
            nr = 201700000 + cs.pk
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
@csrf_exempt
def subscription_photo(request, pk):

    try:
        subscription = CdSubscription.objects.get(pk=pk)
    except CdSubscription.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(content_type=subscription.badgemimetype,
                        data=subscription.badgeimage)

    if request.method == 'POST':
        ps = PhotoSerializer(data=request.data)
        if ps.is_valid():
            try:
                header, data = ps.validated_data.get('imagedata').split(',')
                subscription.badgemimetype = header.split(':')[1].split(';')[0]
                subscription.badgeimage = a2b_base64(data)
                subscription.badgelength = len(subscription.badgeimage)
                subscription.save()
                return Response(status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def belplayer(request, id_national):

    try:
        while id_national.startswith('0'):
            id_national = id_national[1:]
        bp = BelPlayer.objects.get(id_national=id_national)
    except BelPlayer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        if bp.birthdate.year < 1997:
            return Response(status=499)
        bp_serializer = BelplayerSerializer(bp)
        responsedict = dict(bp_serializer.data)
        try:
            cs = CdSubscription.objects.get(id_national=id_national)
            if cs.confirmed:
                responsedict['alreadysubscribed'] = True
        except:
            pass
        return Response(responsedict)

@api_view(['GET'])
def fideplayer(request, id_fide):

    try:
        fp = FidePlayer.objects.get(id_fide=id_fide)
    except FidePlayer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        fp_serializer = FideplayerSerializer(fp)
        return Response(fp_serializer.data)

@api_view(['GET'])
def participants(request, cat):
    players = CdSubscription.objects.filter(category=cat).order_by('-rating')
    data = [{
        'id': p.id,
        'category': p.category,
        'name': p.name,
        'firstname': p.firstname,
        'rating': p.rating,
        'id_club': p.id_club,
        'fidenation': p.fidenation,
        'confirmed': p.confirmed,
    } for p in players]
    return Response(data)

@api_view(['GET', 'POST'])
def mgmtattendees(request):

    if request.method == 'GET':
        param = request.GET
        start = to_int(param.get('start'), 0)
        count = to_int(param.get('count'), 40)
        query = CdSubscription.objects.all()
        cat = param.get('cat')
        if cat:
            query = query.filter(category=cat)
        ss = param.get('ss')
        if ss:
            query = query.filter(name__icontains=ss)
        n_attendees = query.count()
        query = query.order_by('name')[start:start+count]
        result = {
            'ss': ss,
            'cat': cat,
            'start': start,
            'count': count,
            'n_attendees': n_attendees,
            'attendees': [{
                    'id': p.id,
                    'category': p.category,
                    'name': p.name,
                    'firstname': p.firstname,
                    'rating': p.rating,
                    'id_national': p.id_national,
                    'id_club': p.id_club,
                    'fidenation': p.fidenation,
                    'confirmed': p.confirmed,
                    'meals': p.custom1,
                    'present': p.custom2,
                    'payamount': p.payamount,
                } for p in query]
        }
        return Response(result)

    if request.method == 'POST':
        ss = request.data
        try:
            cs = CdSubscription()
            cs.category = ss.get('category')
            cs.chesstitle = ss.get('chesstitle')
            cs.firstname = ss.get('firstname')
            cs.gender = ss.get('gender')
            cs.id_national = '0'
            cs.locale = request.LANGUAGE_CODE.lower()[:2]
            cs.name = ss.get('name')
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
def mgmtattendee_detail(request, id):

    try:
        p = CdSubscription.objects.get(id_national=id)
    except CdSubscription.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        attendee = {
            'id': p.id,
            'category': p.category,
            'name': p.name,
            'firstname': p.firstname,
            'gender': p.gender,
            'rating': p.rating,
            'id_national': p.id_national,
            'id_club': p.id_club,
            'fidenation': p.fidenation,
            'confirmed': p.confirmed,
            'meals': p.custom1,
            'present': p.custom2,
            'payamount': p.payamount,
        }
        return Response(dict(attendee=attendee))

    if request.method == 'PUT':
        data = request.data
        p.name = data.get('name')
        p.firstname = data.get('firstname')
        p.chesstitle = data.get('chesstitle','')
        p.category = data.get('category')
        p.custom1 = data.get('meals')
        p.custom2 = data.get('present')
        p.gender = data.get('gender')
        p.payamount = int(data.get('payamount', 0))
        try:
            p.save()
            return Response(dict(id_national=p.id_national),
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e, status=status.HTTP_406_NOT_ACCEPTABLE)

    if request.method == 'DELETE':
        try:
            p.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(e, status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['GET', 'POST'])
def mgmtattendee_photo(request, id):

    p = None
    try:
        p = CdSubscription.objects.get(id_national=id)
        foundplayer = True
    except CdSubscription.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        if not p or not p.badgelength:
            with open('../cd_subscription/static/img/nobody.png', 'rb') as img:
                return HttpResponse(img.read(), content_type="image/png")
        return HttpResponse(p.badgeimage, content_type=p.badgemimetype)

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

@api_view(['POST'])
def registersms(request):
    """
    register a sms for pairing
    :param request: 
    :return: 
    """
    id_national = request.data.get('id_national')
    mobile = request.data.get('mobile')

    try:
        subscription = CdSubscription.objects.get(id_national=id_national)
    except CdSubscription.DoesNotExist:
        return Response(status=status.HTTP_412_PRECONDITION_FAILED)

    # subscription = CdSubscription()
    # subscription.firstname = "Theo"
    # subscription.name = "Brackx"

    try:
        reg = SmsRegistration.objects.get(id_national=id_national)
        return Response(status=status.HTTP_409_CONFLICT)
    except:
        pass

    reg = SmsRegistration()
    reg.mobile = mobile
    reg.id_national = id_national
    reg.locale = request.LANGUAGE_CODE.lower()[:2]
    reg.save()

    fullname = "{0} {1}".format(subscription.firstname, subscription.name)
    return Response(dict(fullname=fullname, mobile=mobile),
                    status=status.HTTP_201_CREATED)
