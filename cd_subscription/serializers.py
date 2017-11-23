from rest_framework import serializers
from .models import CdSubscription, BelPlayer, FidePlayer

class SubscriptionSerializer(serializers.Serializer):

    category = serializers.CharField()
    emailparent = serializers.CharField(allow_blank=True)
    emailplayer = serializers.CharField(allow_blank=True)
    fullnameattendant = serializers.CharField(allow_blank=True)
    fullnameparent = serializers.CharField(allow_blank=True)
    id_national = serializers.CharField()
    mobileattendant = serializers.CharField(allow_blank=True)
    mobileparent = serializers.CharField(allow_blank=True)


class PhotoSerializer(serializers.Serializer):

    imagedata = serializers.CharField()

class BelplayerSerializer(serializers.ModelSerializer):

    class Meta:

        model = BelPlayer

        fields = (
            'birthdate',
            'chesstitle',
            'federation',
            'firstname',
            'gender',
            'id_club',
            'id_fide',
            'id_national',
            'name',
            'nationality',
            'natrating',
        )

class FideplayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = FidePlayer

        fields = (
            'fiderating',
            'fidenation',
            'firstname',
            'gender',
            'id_fide',
            'name',
        )
