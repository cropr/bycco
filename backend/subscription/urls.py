# original Copyright Ruben Decrop
# modifications by Chessdevil Consulting BVBA

from django.conf.urls import url
from .views import *

urlpatterns = [

    url(r'^$', subscriptionpage),
    url(r'^participants$', participantspage),
    url(r'^mg_attendee$', mg_attendee_page),
    url(r'^mg_attendee_vue$', mg_attendee_vue_page),
    url(r'^mg_presence$', mg_presence_page),
    url(r'^mg_swar$', mg_swar_page),
    url(r'^mg_trn$', mg_trn_page),
    url(r'^view_trn$', view_trn_page),
    url(r'^csv$', csvparticipants),
    url(r'^printbadges$', printbadges),
    url(r'^printallbadges$', printallbadges),
    url(r'^printnamecards$', printnamecards),
    url(r'^printallnamecards$', printallnamecards),
    url(r'^printboardnumbers$', printboardnumbers),
    url(r'^printpairing$', printpairing),
    url(r'^printprizes/(?P<categories>.+)$', printprizes),
]

