#    Copyright 2017 - 2018 Ruben Decrop
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import logging
log = logging.getLogger(__name__)

import simplejson as json
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.conf import settings # import the settings file
from django import forms
from django.db.models import Q
from bycco.context_processor import locale_msg

import datetime

from .models import (
    ByccoMarkdownView, ByccoArticlesIntroView, ByccoArticle, ByccoArticleLocale
)

@plugin_pool.register_plugin
class ByccoMarkdownPlugin(CMSPluginBase):

    model = ByccoMarkdownView
    name = 'Markdown page'
    module = 'Bycco'
    render_template = 'byccoarticles/markdown.html'

    def render(self, context, instance, placeholder):
        context['source'] = instance.source
        context['sanitize'] = instance.sanitize
        return super(ByccoMarkdownPlugin, self).render(
            context, instance, placeholder) 

@plugin_pool.register_plugin
class ByccoArticlesIntroPlugin(CMSPluginBase):

    model = ByccoArticlesIntroView
    name = 'Intro of articles'
    module = 'Bycco'
    render_template = 'byccoarticles/introview.html'

    def render(self, context, instance, placeholder):
        now = datetime.datetime.utcnow()
        qa = ByccoArticle.objects.all().exclude(published__isnull=True)
        qa = qa.filter(published__lt=now)
        qa = qa.filter(Q(archived__isnull=True) | Q(archived__gt=now))
        articles = list(qa.order_by('-published')
            [ instance.start:instance.start+instance.count]
        )
        lang = context.get('LANGUAGE_CODE')
        context['articles'] = []
        for a in articles:
            localefields = a.localefields.filter(locale=lang).all()
            if localefields and localefields[0].title:
                a.title = localefields[0].title
            else: 
                a.title = a.maintitle
            if localefields and localefields[0].intro:
                a.intro = localefields[0].intro
            else:
                a.intro = locale_msg[lang]['_OL']
                a.readmore = True
            context['articles'].append(a) 
        return super(ByccoArticlesIntroPlugin, self).render(
            context, instance, placeholder)
