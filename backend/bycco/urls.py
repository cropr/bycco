# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from .views import test

import tournament.apiurls
import tournament.urls

admin.autodiscover()

urlpatterns = [
    # path('sitemap.xml', sitemap,
    #     {'sitemaps': {'cmspages': CMSSitemap}}),
    path('api/', include(tournament.apiurls)),
    # url(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('trn', include(tournament.urls)),
    path('trn/', include(tournament.urls)),

    # to avoid redirecting 404s in /api/* to /{locale}/api/*
    # next url pattern has a negative lookahead pattern
    re_path(r'^(?!api)', include('cms.urls')),
)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

