# original Copyright Ruben Decrop
# modifications by Chessdevil Consulting BVBA

from django.conf.urls import url
from .views import *

urlpatterns = [

    url(r'^$', subscriptionpage),
    url(r'^participants$', participantspage),
    url(r'^attendee$', mgmtattendeepage),
    url(r'^csv$', csvparticipants),
    url(r'^sms$', smspage),
    url(r'^printbadges$', printbadges),
    url(r'^printallbadges$', printallbadges),
    url(r'^printnamecards$', printnamecards),
    url(r'^printallnamecards$', printallnamecards),
    url(r'^printallnamecardsgirls$', printallnamecardsgirls),
    url(r'^printboardnumbers$', printboardnumbers),

]

