from rest_framework import serializers
from .models import *

class SubscriptionSerializer(serializers.Serializer):

    category = serializers.CharField()
    emailparent = serializers.CharField(allow_blank=True)
    emailplayer = serializers.CharField(allow_blank=True)
    fullnameattendant = serializers.CharField(allow_blank=True)
    fullnameparent = serializers.CharField(allow_blank=True)
    idbel = serializers.CharField()
    mobileattendant = serializers.CharField(allow_blank=True)
    mobileparent = serializers.CharField(allow_blank=True)


class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CdTournament

        fields = (
            'id',
            'name',
            'shortname',
            'rounds',
        )


class SwarTournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CdSwarTournament

        fields = (
            'swarname',
        )


class SwarJsonSerializer(serializers.ModelSerializer):
    class Meta:
        model = CdSwarJson

        fields = (
            'id',
            'name',
            'round',
            'jsonfile',
            'tournament',
            'uploaddate',
            'status',
        )


class SwarJsonSerializerSmall(serializers.ModelSerializer):
    class Meta:
        model = CdSwarJson

        fields = (
            'id',
            'name',
            'round',
            'tournament',
            'uploaddate',
            'status',
        )