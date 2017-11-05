# Copyright 2014 Ruben Decrop

from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import BelPlayer, FidePlayer
from .serializers import BelplayerSerializer, FideplayerSerializer
import requests


@api_view(['GET'])
def belmember(request, id_national):

    if request.method == 'GET':
        rc = requests.get('http://www.frbe-kbsb.be/sites/manager/api/players.php',
                         params={'id': id_national})
        replies = rc.json()
        if len(replies):
            return Response({'member': replies[0]})
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def belplayer(request, id_national):

    try:
        while id_national.startswith('0'):
            id_national = id_national[1:]
        bp = BelPlayer.objects.get(id_national=id_national)
    except BelPlayer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response({"player": BelplayerSerializer(bp).data})

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def fideplayer(request, id_fide):

    try:
        fp = FidePlayer.objects.get(id_fide=id_fide)
    except FidePlayer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        fp_serializer = FideplayerSerializer(fp)
        return Response(fp_serializer.data)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)