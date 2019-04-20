# original Copyright Ruben Decrop
# modifications by Chessdevil Consulting BVBA

from django.conf.urls import url
from .views import *

urlpatterns = [

    url(r'^$', subscriptionpage),
    url(r'^subscription$', subscriptionpage),
    url(r'^participants$', participantspage),
    url(r'^management$', managementpage),
    url(r'^view$', trnviewpage),
    url(r'^aboutus$', aboutuspage),
    url(r'^csv$', csvparticipants),
    url(r'^printbadges$', printbadges),
    url(r'^printnamecards$', printnamecards),
    url(r'^printboardnumbers$', printboardnumbers),
    # url(r'^podiumphotos$', podiumphotos),
    url(r'^printprizes/(?P<cat>.+)$', printprizes),
]

