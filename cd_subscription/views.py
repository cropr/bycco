# Copyright Ruben Decrop

import logging
log = logging.getLogger(__name__)

import csv
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import CdSubscription

def subscriptionpage(request):
    return render(request, 'cd_subscription/subscriptionpage.html')

def participantspage(request):
    return render(request, 'cd_subscription/participants.html')

def mgmtattendeepage(request):
    return render(request, 'cd_subscription/mgmtattendee.html')

def printbadges(request):
    """
    :param request: 
    :return: 
    """
    ids = request.GET
    pages = []
    badges = []
    j = 0
    for id in ids:
        try:
            p = CdSubscription.objects.get(id_national=id)
        except CdSubscription.DoesNotExist:
            continue
        rix = j % 2 + 1
        cix = j // 2 + 1
        badge = {
            'name': p.name,
            'firstname': p.firstname,
            'rating': p.rating or "",
            'chesstitle': p.chesstitle + " " if p.chesstitle else "",
            'category': p.category,
            'meals': p.custom1,
            'mealsclass': "badge_{}".format(p.custom1 or "NM"),
            'color': p.category,
            'photourl': 'cd_subscription/api/attendee/{0}/photo'.format(
                p.id_national),
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
    return render(request, 'cd_subscription/printbadge.html', {'pages': pages})

def printallbadges(request):
    """
    :param request: 
    :return: 
    """
    ids = request.POST.get('ids')
    pages = []
    badges = []
    j = 0
    for p in CdSubscription.objects.all().order_by('category','name'):
        rix = j % 2 + 1
        cix = j // 2 + 1
        badge = {
            'name': p.name,
            'firstname': p.firstname,
            'rating': p.rating or "",
            'chesstitle': p.chesstitle + " " if p.chesstitle else "",
            'category': p.category,
            'meals': p.custom1,
            'mealsclass': "badge_{}".format(p.custom1 or "NM"),
            'color': p.category,
            'photourl': 'cd_subscription/api/attendee/{0}/photo'.format(
                p.id_national),
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
    return render(request, 'cd_subscription/printbadge.html', {'pages': pages})

def printnamecards(request):
    """
    :param request: 
    :return: 
    """
    ids = request.GET
    pages = []
    cards = []
    j = 0
    for id in ids:
        try:
            p = CdSubscription.objects.get(id_national=id)
        except CdSubscription.DoesNotExist:
            continue
        rix = j % 2 + 1
        ct = p.chesstitle + " " if p.chesstitle else ""
        card = {
            'fullname': "{0}{1} {2}".format(ct, p.name, p.firstname),
            'natrating': p.natrating or "0",
            'fiderating': p.fiderating or "0",
            'category': p.category,
            'color': p.category,
            'locale': p.locale,
            'photourl': 'cd_subscription/api/attendee/{0}/photo'.format(
                p.id_national),
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
    return render(request, 'cd_subscription/printnamecard.html', {'pages': pages})

def printallnamecards(request):
    """
    :param request: 
    :return: 
    """
    ids = request.POST.get('ids')
    pages = []
    cards = []
    j = 0
    for p in CdSubscription.objects.all().order_by('category','name'):
        if not p.category.startswith('B'):
            continue
        rix = j % 2 + 1
        ct = p.chesstitle + " " if p.chesstitle else ""
        card = {
            'fullname': "{0}{1} {2}".format(ct, p.name, p.firstname),
            'natrating': p.natrating or "0",
            'fiderating': p.fiderating or "0",
            'category': p.category,
            'color': p.category,
            'locale': p.locale,
            'photourl': 'cd_subscription/api/attendee/{0}/photo'.format(
                p.id_national),
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
    return render(request, 'cd_subscription/printnamecard.html',
                  {'pages': pages})

def printallnamecardsgirls(request):
    """
    :param request: 
    :return: 
    """
    ids = request.POST.get('ids')
    pages = []
    cards = []
    j = 0
    for p in CdSubscription.objects.all().order_by('category','name'):
        if not p.category.startswith('G'):
            continue
        rix = j % 2 + 1
        ct = p.chesstitle + " " if p.chesstitle else ""
        card = {
            'fullname': "{0}{1} {2}".format(ct, p.name, p.firstname),
            'natrating': p.natrating or "0",
            'fiderating': p.fiderating or "0",
            'category': p.category,
            'color': p.category,
            'locale': p.locale,
            'photourl': 'cd_subscription/api/attendee/{0}/photo'.format(
                p.id_national),
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
    return render(request, 'cd_subscription/printnamecard.html',
                  {'pages': pages})

def printboardnumbers(request):
    """
    :param request: 
    :return: 
    """
    pages = []
    page = []
    counters = {}

    for p in CdSubscription.objects.all():
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
    return render(request, 'cd_subscription/printboardnr.html',
                  {'pages': pages})

def smspage(request):
    return render(request, 'cd_subscription/subscribesms.html')

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
        'fidenation',
        'fiderating',
        'firstname',
        'fullnameattendant',
        'fullnameparent',
        'gender',
        'id_club',
        'id_fide',
        'id_national',
        'locale',
        'mobileattendant',
        'mobileparent',
        'mobileplayer',
        'name',
        'nationality',
        'natrating',
        'payamount',
        'paydate',
        'paymessage',
        'rating',
        'remarks',
        'custom1',
        'custom2',
        'custom3',
    ]
    writer = csv.writer(response)
    writer.writerow(fields)
    for s in CdSubscription.objects.all():
        values = [str(getattr(s, f)) for f in fields]
        writer.writerow(values)
    return response
