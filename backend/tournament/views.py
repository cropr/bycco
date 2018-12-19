# Copyright Ruben Decrop

import logging
log = logging.getLogger(__name__)

import csv
import simplejson as json
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _


from .models import (
    CdSwarTournament,
    CdSwarJson,
    CdTournament,
    CdTournamentPrizes,
    Subscription
)

translations = {
    'Category': _('Category'),
    'Files': _('Files'),
    'Live Games': _('Live Games'),
    'Pairings': _('Pairings'),
    'Round': _('Round'),
    'Standings': _('Standings'),
    'Tournament Results': _('Tournament Results'),
}

def subscriptionpage(request):
    return render(request, 'tournament/subscriptionpage.html')

# def participantspage(request):
#     return render(request, 'subscription/participants.html')
#
# def mg_attendee_page(request):
#     return render(request, 'subscription/mg_attendee.html')
#
# def mg_attendee_vue_page(request):
#     return render(request, 'subscription/mg_attendee_vue.html')
#
# def mg_presence_page(request):
#     return render(request, 'subscription/mg_presence.html')
#
# def mg_swar_page(request):
#     return render(request, 'subscription/mg_swar.html')
#
# def mg_trn_page(request):
#     return render(request, 'subscription/mg_trn.html')

def participantspage(request):
    return render(request, 'tournament/participantspage.html')

def managementtpage(request):
    return render(request, 'tournament/managementtpage.html')


def printbadges(request):
    """
    :param request: 
    :return: 
    """
    ids = request.GET.get('ids')
    pages = []
    badges = []
    j = 0
    for id in ids.split(','):
        try:
            p = Subscription.objects.get(id=id)
        except Subscription.DoesNotExist:
            continue
        rix = j % 2 + 1
        cix = j // 2 + 1
        badge = {
            'last_name': p.last_name,
            'first_name': p.first_name,
            'rating': p.rating or "",
            'chesstitle': p.chesstitle + " " if p.chesstitle else "",
            'category': p.category,
            'meals': p.custom1,
            'mealsclass': "badge_{}".format(p.custom1 or "NM"),
            'color': p.category,
            'photourl': '/api/photo/{0}'.format(p.id),
            'positionclass': 'badge{0}{1}'.format(cix, rix)
        }
        badges.append(badge)
        j += 1
        if j == 8:
            j = 0
            pages.append(badges)
            badges = []
    if j > 0:
        pages.append(badges)
    return render(request, 'subscription/printbadge.html', {'pages': pages})

def printallbadges(request):
    """
    :param request: 
    :return: 
    """
    pages = []
    badges = []
    j = 0
    for p in Subscription.objects.all().order_by('category','last_name'):
        rix = j % 2 + 1
        cix = j // 2 + 1
        badge = {
            'last_name': p.last_name,
            'first_name': p.first_name,
            'rating': p.rating or "",
            'chesstitle': p.chesstitle + " " if p.chesstitle else "",
            'category': p.category,
            'meals': p.custom1,
            'mealsclass': "badge_{}".format(p.custom1 or "NM"),
            'color': p.category,
            'photourl': '/api/photo/{0}'.format(p.id),
            'positionclass': 'badge{0}{1}'.format(cix, rix)
        }
        badges.append(badge)
        j += 1
        if j == 8:
            j = 0
            pages.append(badges)
            badges = []
    if j > 0:
        pages.append(badges)
    return render(request, 'subscription/printbadge.html', {'pages': pages})

def printnamecards(request):
    """
    :param request: 
    :return: 
    """
    ids = request.GET.get('ids')
    pages = []
    cards = []
    j = 0
    for id in ids.split(','):
        try:
            p = Subscription.objects.get(id=id)
        except Subscription.DoesNotExist:
            continue
        rix = j % 2 + 1
        ct = p.chesstitle + " " if p.chesstitle else ""
        card = {
            'fullname': "{0}{1} {2}".format(ct, p.last_name, p.first_name),
            'natrating': p.ratingbel or "0",
            'fiderating': p.ratingfide or "0",
            'category': p.category,
            'color': p.category,
            'locale': p.locale,
            'photourl': '/api/photo/{0}'.format(p.id),
            'positionclass': 'card_1{0}'.format(rix)
        }
        cards.append(card)
        j += 1
        if j == 2:
            j = 0
            pages.append(cards)
            cards = []
    if j > 0:
        pages.append(cards)
    return render(request, 'subscription/printnamecard.html', {'pages': pages})

def printallnamecards(request):
    """
    :param request: 
    :return: 
    """
    ids = request.POST.get('ids')
    pages = []
    cards = []
    j = 0
    for p in Subscription.objects.all().order_by('category','last_name'):
        rix = j % 2 + 1
        ct = p.chesstitle + " " if p.chesstitle else ""
        card = {
            'fullname': "{0}{1} {2}".format(ct, p.last_name, p.first_name),
            'natrating': p.ratingbel or "0",
            'fiderating': p.ratingfide or "0",
            'category': p.category,
            'color': p.category,
            'locale': p.locale,
            'photourl': '/api/photo/{0}'.format(p.id),
            'positionclass': 'card_1{0}'.format(rix)
        }
        cards.append(card)
        j += 1
        if j == 2:
            j = 0
            pages.append(cards)
            cards = []
    if j > 0:
        pages.append(cards)
    return render(request, 'subscription/printnamecard.html', {'pages': pages})

def printboardnumbers(request):
    """
    :param request: 
    :return: 
    """
    pages = []
    page = []
    counters = {}

    for p in Subscription.objects.all():
        cc = counters.get(p.category, 0)
        counters[p.category] = cc + 1
    cats = (
        ("B8", "G8"),
        ("B10",),
        ("G10", ),
        ("B12", ),
        ("G12", ),
        ("B14", ),
        ("G14", ),
        ("B16", ),
        ("G16", ),
        ("B18", "G18"),
        ("B20", "G20"),
    )
    counter = 0
    for cat in cats:
        nrcards = sum((counters.get(subcat, 0)) for subcat in cat)
        for j in range(nrcards // 2 + 2):
            rix = counter % 3 + 1
            cix = counter // 3 + 1
            card = {
                'ix': j + 1,
                'category': cat[0],
                'positionclass': 'bnr_{0}{1}'.format(cix, rix)
            }
            page.append(card)
            counter += 1
            if counter >= 15:
                pages.append(page)
                page = []
                counter = 0
    if counter > 0:
        pages.append(page)
    return render(request, '/subscription/printboardnr.html',
                  {'pages': pages})

def printpairing(request):
    """
    :param request:
    :return:
    """
    from .swarconvert import pairingsfromswar
    id_swarfile = request.GET.get('id_swarfile')
    try:
        swarfile = CdSwarJson.objects.get(id=id_swarfile)
    except CdSwarJson.DoesNotExist:
        return "Swarfile not found"
    trnname = swarfile.swartrn.tournament.name
    trncolor = swarfile.swartrn.tournament.shortname
    round = swarfile.round
    swarjson = json.loads(swarfile.jsonfile)
    pairings = pairingsfromswar(swarjson)
    return render(request, 'subscription/printpairing.html', {
        'trnname': trnname,
        'trncolor': trncolor,
        'pairings': pairings,
        'round': round,
    })

def printprizes(request, cat):
    try:
        trn = CdTournament.objects.get(shortname=cat)
        if hasattr(trn, "cdtournamentprizes"):
            prizes = json.loads(trn.cdtournamentprizes.jsonprizes).get(
                'playerprizes', [])
    except CdTournament.DoesNotExist:
        prizes = []
    cards = []
    pages = []
    j = 0
    for p in prizes:
        rix = j % 3 + 1
        p['positionclass'] = 'prize_1{0}'.format(rix)
        j += 1
        cards.append(p)
        if j == 3:
            j = 0
            pages.append(cards)
            cards = []
    if j > 0:
        pages.append(cards)
    return render(request, 'subscription/printprize.html', dict(pages=pages))

@login_required
def csvparticipants(request):
    """
    cretae a csv file of all participants
    :param request:
    :return:
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="participants.csv"'

    fields = [
        'badgelength',
        'birthdate',
        'category',
        'chesstitle',
        'confirmed',
        'emailparent',
        'emailplayer',
        'federation',
        'first_name',
        'fullnameattendant',
        'fullnameparent',
        'gender',
        'idbel',
        'idclub',
        'idfide',
        'last_name',
        'locale',
        'mobileattendant',
        'mobileparent',
        'mobileplayer',
        'nationalitybel',
        'nationalityfide',
        'payamount',
        'paydate',
        'paymessage',
        'rating',
        'ratingbel',
        'ratingfide',
        'custom1',
        'custom2',
        'custom3',
    ]
    writer = csv.writer(response)
    writer.writerow(fields)
    for s in Subscription.objects.all():
        values = [str(getattr(s, f)) for f in fields]
        writer.writerow(values)
    return response
