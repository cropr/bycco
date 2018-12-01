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

class ParticipantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription

        fields = [
            'id', 'first_name', 'last_name', 'category', 'ratingbel',
            'ratingfide', 'gender',
        ]

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
            'tournament_id',
        )


class SwarJsonSerializer(serializers.ModelSerializer):
    class Meta:
        model = CdSwarJson

        fields = (
            'id',
            'round',
            'jsonfile',
            'swartrn',
            'uploaddate',
            'status',
        )


class SwarJsonSerializerSmall(serializers.ModelSerializer):
    class Meta:
        model = CdSwarJson

        fields = (
            'id',
            'round',
            'swartrn',
            'uploaddate',
            'status',
        )

class UploadSwarJsonSerializer(serializers.Serializer):
    id_trn = serializers.IntegerField()
    name = serializers.CharField()
    jsonfile = serializers.CharField()
    round = serializers.IntegerField()