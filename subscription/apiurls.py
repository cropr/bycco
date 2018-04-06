# original Copyright Ruben Decrop
# modifications by Chessdevil Consulting BVBA

from django.conf.urls import url
from subscription import apiviews

urlpatterns = [
    url(r'attendees$', apiviews.attendee_all),
    url(r'attendees/(?P<id>\w+)$', apiviews.attendee_detail),
    url(r'attendees/(?P<idsub>[0-9]+)/resend$',
        apiviews.subscription_resend),
    url(r'belplayer/(?P<idbel>[0-9]+)$', apiviews.belplayer),
    url(r'fideplayer/(?P<idfide>[0-9]+)$', apiviews.fideplayer),
    url(r'photo/(?P<id>[0-9]+)$', apiviews.attendee_photo),
    url(r'subscriptions$', apiviews.subscription_all),
    url(r'subscriptions/(?P<idsub>[0-9]+)/photo$', apiviews.subscription_photo),
    url(r'subscriptions/(?P<idsub>[0-9]+)/confirm$',
        apiviews.subscription_confirmation),
    url(r'^tournament$', apiviews.tournament_all),
    url(r'^tournament/(?P<id_trn>[0-9]+)$', apiviews.tournament_one),
    url(r'^tournament/(?P<id_trn>[0-9]+)/pairings/(?P<round>[0-9]+)$',
        apiviews.tournament_pairings),
    url(r'^tournament/(?P<id_trn>[0-9]+)/standings/(?P<round>[0-9]+)$',
        apiviews.tournament_standings),
    url(r'^tournament/(?P<id_trn>[0-9]+)/playercard/(?P<id_player>[0-9]+)$',
        apiviews.tournament_playercard),
    url(r'^tournament/(?P<id_trn>[0-9]+)/prizes$',
        apiviews.tournament_prizes),
    url(r'^tournament/(?P<id_trn>[0-9]+)/swar$', apiviews.tournament_swar),
    url(r'^swar$', apiviews.swartrn_all),
    url(r'^swar/(?P<id_swartrn>[0-9]+)$', apiviews.swartrn_one),
    url(r'^swar/(?P<id_swartrn>[0-9]+)/publication/(?P<id_swarfile>[0-9]+)$',
        apiviews.swarfile_publication),
    url(r'^swar/(?P<id_swartrn>[0-9]+)/file$', apiviews.swarfile_all),
    url(r'^swar/(?P<id_swartrn>[0-9]+)/file/(?P<id_swarfile>[0-9]+)$',
        apiviews.swarfile_one),
    url(r'^swarn/(?P<id_swartrn>[0-9]+)/topround$', apiviews.topround),

]

