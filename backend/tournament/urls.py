# original Copyright Ruben Decrop
# modifications by Chessdevil Consulting BVBA

from django.urls import path
from .views import *

urlpatterns = [

    path('/', subscriptionpage),
    path('subscription', subscriptionpage),
    path('participants', participantspage),
    path('management', managementpage),
    path('view', trnviewpage),
    path('aboutus', aboutuspage),
    path('csv', csvparticipants),
    path('printbadges', printbadges),
    path('printnamecards', printnamecards),
    path('printboardnumbers', printboardnumbers),
    path('podiumphotos', podiumphotos),
    path('printprizes/<str:cat>', printprizes),
]

