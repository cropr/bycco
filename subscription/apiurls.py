# original Copyright Ruben Decrop
# modifications by Chessdevil Consulting BVBA

from django.conf.urls import url
from subscription import apiviews

urlpatterns = [
    url(r'attendees$', apiviews.attendee_all),
    url(r'attendees/(?P<id>\w+)$', apiviews.attendee_detail),
    url(r'belplayer/(?P<idbel>[0-9]+)$', apiviews.belplayer),
    url(r'fideplayer/(?P<idfide>[0-9]+)$', apiviews.fideplayer),
    url(r'photo/(?P<id>[0-9]+)$', apiviews.attendee_photo),
    url(r'subscriptions$', apiviews.subscription_all),
    url(r'subscriptions/(?P<idsub>[0-9]+)/photo$', apiviews.subscription_photo),
    url(r'subscriptions/(?P<idsub>[0-9]+)/confirm$',
        apiviews.subscription_confirmation),
]

