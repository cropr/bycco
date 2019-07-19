# Copyright Ruben Decrop

import logging
log = logging.getLogger(__name__)

import requests
import iso8601
import simplejson as json
from django.db.models import Max
from django.shortcuts import redirect
from django.conf import settings
from django.utils import  translation

from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import BaseRenderer, JSONRenderer
from slugify import slugify

from .models import (
    ByccoArticle,
    ByccoArticleLocale,
)

def datetostr(d):
    """
    return a isostr from a date or None
    """
    if d:
        return d.strftime("%Y-%m-%d %H:%M:%S")

def strtodate(s):
    """
    return a datetime from a str or None
    """
    try:
        return iso8601.parse_date(s)
    except iso8601.ParseError:
        return

@api_view(['POST', 'GET'])
def article_all(request):

    if request.method == 'GET':
        articles = ByccoArticle.objects.all()
        lang = translation.get_language()
        introrequired = request.GET.get('intro')
        als = []
        for a in articles:
            ad = {
                'id': a.id,
                'maintitle': a.maintitle,
                'author': a.author,
                'published': datetostr(a.published),
                'slug': a.slug,
            }
            for l in a.localefields.all():
                if l.locale == lang:
                    ad['title'] = l.title
                    if introrequired:
                        ad['intro'] = l.intro            
            als.append(ad)
        return Response(dict(articles=als))

    if request.method == 'POST':
        """
        article should contain: maintitle, mainlocale
        """
        data = request.data.get('article', {})
        log.info('article input %s', data)
        a = ByccoArticle()
        a.mainlocale = data.get('mainlocale')
        a.maintitle = data.get('maintitle')
        if not a.mainlocale or not a.maintitle:
            return Response('MissingField', 
                status=status.HTTP_400_BAD_REQUEST)
        a.author = data.get('author', 'nobody')
        a.archived = None
        a.published = None
        a.slug = slugify(a.maintitle)
        al = ByccoArticleLocale()
        al.locale = a.mainlocale
        al.title = a.maintitle
        try:
            a.save()
            al.article = a
            al.save()
        except Exception as e:
            return Response('ArticleNotSaved', 
                status=status.HTTP_400_BAD_REQUEST)
        return Response(dict(id=a.id), status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def article_one(request, id):

    try:
        a = ByccoArticle.objects.get(id=id)
    except ByccoArticle.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        art = {
            'author': a.author,
            'created':  datetostr(a.created),
            'archived':  datetostr(a.archived),
            'mainlocale':  a.mainlocale,
            'maintitle':  a.maintitle,
            'modified': datetostr(a.modified),
            'readmore': a.readmore,
            'published': datetostr(a.published),

            'slug': a.slug,         
        }
        for al in ByccoArticleLocale.objects.filter(article=a):
            art[al.locale] = {
                'content': al.content,
                'intro': al.intro,
                'title': al.title,
            }
        return Response(dict(article=art))

    if request.method == 'PUT':
        data = request.data.get('article', {})
        a.author = data.get('author', a.author)
        a.archived = strtodate(data['archived']) if \
            'archived' in data else a.archived
        a.mainlocale = data.get('mainlocale', a.mainlocale)
        a.readmore = data.get('readmore', a.readmore)
        a.published = strtodate(data['published']) if \
            'published' in data else a.published
        a.slug = data.get('slug', a.slug)
        als = []
        for l in ('en', 'fr', 'de', 'nl'):
            if l in data:
                try:
                    al = ByccoArticleLocale.objects.get(article=a, locale=l)
                except ByccoArticleLocale.DoesNotExist:
                    al = ByccoArticleLocale(article=a, locale=l)
                lf = data[l]
                al.title = lf.get('title', al.title or '')
                al.content = lf.get('content', al.content or '')
                al.intro = lf.get('intro', al.intro or '')
                if a.mainlocale == l:
                    a.maintitle = al.title
                als.append(al)
        try:
            a.save()
            for al in als: 
                al.save()
        except Exception as e:
            log.exception("could not update member")
            return Response(e, status=status.HTTP_406_NOT_ACCEPTABLE)
        art = {
            'author': a.author,
            'created':  datetostr(a.created),
            'archived':  datetostr(a.archived),
            'mainlocale':  a.mainlocale,
            'modified': datetostr(a.modified),
            'readmore': a.readmore,
            'published': datetostr(a.published),
            'slug': a.slug,         
        }
        for al in ByccoArticleLocale.objects.filter(article=a):
            art[al.locale] = {
                'content': al.content,
                'intro': al.intro,
                'title': al.title,
            }
        return Response(dict(article=json.dumps(art)))
        
    if request.method == 'DELETE':
        a.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

