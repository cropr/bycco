import os

gettext = lambda s: s

ALLOWED_HOSTS = ['*']

APPEND_SLASH = False

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CKEDITOR_SETTINGS = {
    'stylesSet': [
        {'name': 'carousel caption', 'element': 'div', 'attributes': {
            'class': 'carouselcaption'
        }}
    ],
}

CMS_LANGUAGES = {
    1: [
        {
            'name': gettext('en'),
            'public': True,
            'redirect_on_fallback': True,
            'hide_untranslated': False,
            'code': 'en',
        },
        {
            'name': gettext('nl'),
            'public': True,
            'redirect_on_fallback': True,
            'hide_untranslated': False,
            'code': 'nl',
        },
        {
            'name': gettext('fr'),
            'public': True,
            'redirect_on_fallback': True,
            'hide_untranslated': False,
            'code': 'fr',
        },
        {
            'name': gettext('de'),
            'public': True,
            'redirect_on_fallback': True,
            'hide_untranslated': False,
            'code': 'de',
        },
    ],
    'default': {
        'public': True,
        'redirect_on_fallback': True,
        'hide_untranslated': False,
    },
}

CMS_TEMPLATES = (
    ('vuecms.html', 'Cms Page'),
    ('landing.html', 'LandingPage'),
    ('page.html', 'Page'),
)

CMS_PERMISSION = True

CMS_PLACEHOLDER_CONF = {}

DATA_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASES = {   # dummy for collectstatic
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'localhost',
        'NAME': 'bycco',
        'USER': '',
        'PASSWORD': '',
    }
}


DEBUG = True

EMAIL_HOST = 'localhost'
EMAIL_PORT = 25

INSTALLED_APPS = (

    # django + cms admin
    'djangocms_admin_style',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django_tablib',

    # djangocms
    'cms',
    'filer',
    'easy_thumbnails',
    'cmsplugin_filer_file',
    'cmsplugin_filer_folder',
    'cmsplugin_filer_image',
    'cmsplugin_filer_teaser',
    'cmsplugin_filer_utils',
    'cmsplugin_filer_video',
    'menus',
    'sekizai',
    'treebeard',
    'djangocms_text_ckeditor',
    'djangocms_style',
    'djangocms_file',
    'djangocms_googlemap',
    'djangocms_inherit',
    'djangocms_link',
    'reversion',

    # my apps
    # 'subscription',
    'webpack_loader',
    'rd_django',
    'bycco'
)

LANGUAGE_CODE = 'nl'
LANGUAGES = (
    ## Customize this
    ('en', gettext('en')),
    ('nl', gettext('nl')),
    ('fr', gettext('fr')),
    ('de', gettext('de')),
)

LOCALE_PATHS = (os.path.join(BASE_DIR, 'i18n'),)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'bycco': {
            'level': 'DEBUG',
            'handlers': ['console']
        },
        'subscription': {
            'level': 'DEBUG',
            'handlers': ['console']
        },
        'django' : {
            'level': 'INFO',
            'handlers': ['console'],
        }
    },
}


MEDIA_ROOT = os.path.join(DATA_DIR, 'media')
MEDIA_URL = '/media/'

META_SITE_PROTOCOL = 'https'
META_USE_SITES = True

MIDDLEWARE_CLASSES = (
    'cms.middleware.utils.ApphookReloadMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware'
)

MIGRATION_MODULES = {

}

# PARLER_LANGUAGES = {
#     1: (
#         {'code': 'nl',},
#         {'code': 'en',},
#         {'code': 'fr', },
#         {'code': 'de', },
#     ),
#     'default': {
#         'fallbacks': ['nl', 'fr', 'de'],
#     }
# }

PRODUCTION = True
# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': [],
#     'DEFAULT_PERMISSION_CLASSES': [],
# }

ROOT_URLCONF = 'bycco.urls'

SECRET_KEY = 'kustabitjevierkantigmekloten'

SITE_ID = 1

STATIC_ROOT = 'static'
STATIC_URL = '/static/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'bycco', 'templates'),],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.csrf',
                'django.template.context_processors.tz',
                'sekizai.context_processors.sekizai',
                'django.template.context_processors.static',
                'cms.context_processors.cms_settings',
                'bycco.util.production_settings',
                # 'zinnia.context_processors.version',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                'django.template.loaders.eggs.Loader'
            ],
        },
    },
]

TIME_ZONE = 'Europe/Brussels'

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters'
)

USE_I18N = True

USE_L10N = True

USE_TZ = True

WSGI_APPLICATION = 'bycco.wsgi.application'

try:
    from local_settings import *
    print('local_settings read')
except ImportError:
    print('No local settings found')
