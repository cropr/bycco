from rest_framework import serializers
from .models import Subscription

class SubscriptionSerializer(serializers.Serializer):

    category = serializers.CharField()
    emailparent = serializers.CharField(allow_blank=True)
    emailplayer = serializers.CharField(allow_blank=True)
    fullnameattendant = serializers.CharField(allow_blank=True)
    fullnameparent = serializers.CharField(allow_blank=True)
    idbel = serializers.CharField()
    mobileattendant = serializers.CharField(allow_blank=True)
    mobileparent = serializers.CharField(allow_blank=True)
