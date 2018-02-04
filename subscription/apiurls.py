# original Copyright Ruben Decrop
# modifications by Chessdevil Consulting BVBA

from django.conf.urls import url
from subscription import apiviews

urlpatterns = [

    # url(r'$', subscription_list),
    url(r'belplayer/(?P<idbel>[0-9]+)$', apiviews.belplayer),
    url(r'fideplayer/(?P<idfide>[0-9]+)$', apiviews.fideplayer),
    url(r'subscriptions$', apiviews.subscriptions),
    url(r'subscriptions/(?P<idsub>[0-9]+)/photo$', apiviews.subscription_photo),
    url(r'subscriptions/(?P<idsub>[0-9]+)/confirm$',
        apiviews.subscription_confirmation),
    # url(r'/detail/(?P<pk>[0-9]+)/$', subscription_detail),
    # url(r'/participants/(?P<cat>.+)$', participants),
    url(r'attendees$', apiviews.mgmtattendees),
    url(r'attendees/(?P<id>\w+)$', apiviews.mgmtattendee_detail),
    # url(r'attendees/(?P<id>[0-9]+)/photo$', mgmtattendee_photo),
]

