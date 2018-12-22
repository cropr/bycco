# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve

from .views import test_base, test_cms, test_vue, test_vuecms

import tournament.apiurls
import tournament.urls

admin.autodiscover()

urlpatterns = [
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': {'cmspages': CMSSitemap}}),
    url(r'^api/', include(tournament.apiurls)),
    # url(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
]

urlpatterns += i18n_patterns(
    url(r'^admin/', include(admin.site.urls)),
    url('accounts/', include('django.contrib.auth.urls')),
    url(r'^trn', include(tournament.urls)),
    url(r'^trn/', include(tournament.urls)),


    # to avoid redirecting 404s in /api/* to /{locale}/api/*
    # next url pattern has a negative lookahead pattern
    url(r'^(?!api)', include('cms.urls')),
)
# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns = [
        url(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        ] + staticfiles_urlpatterns() + urlpatterns
