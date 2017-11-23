# original Copyright Ruben Decrop
# modifications by Chessdevil Consulting BVBA

from django.conf.urls import url
from .apiviews import *

urlpatterns = [

    url(r'$', subscription_list),
    url(r'/detail/(?P<pk>[0-9]+)/$', subscription_detail),
    url(r'/confirmation/(?P<pk>[0-9]+)$', subscription_confirmation),
    url(r'/photo/(?P<pk>[0-9]+)$', subscription_photo),
    url(r'/participants/(?P<cat>.+)$', participants),
    url(r'/attendee$', mgmtattendees),
    url(r'/attendee/(?P<id>[0-9]+)$', mgmtattendee_detail),
    url(r'/attendee/(?P<id>[0-9]+)/photo$', mgmtattendee_photo),
]

