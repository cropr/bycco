import os

ALLOWED_HOSTS = ['*']

APPEND_SLASH = False

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CHESSAPI_URL = 'https://chessapi.bycco.be/'

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
            'name': 'en',
            'public': True,
            'redirect_on_fallback': True,
            'hide_untranslated': False,
            'code': 'en',
        },
        {
            'name': 'nl',
            'public': True,
            'redirect_on_fallback': True,
            'hide_untranslated': False,
            'code': 'nl',
        },
        {
            'name': 'fr',
            'public': True,
            'redirect_on_fallback': True,
            'hide_untranslated': False,
            'code': 'fr',
        },
        {
            'name': 'de',
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
EMAIL_ADDRESSES = {
    'invoice_from': 'info@bycco.be',
    'invoice_cc': ['ruben@decrop.net', 'mj.deschepper@gmail.com'],
}

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

    # blog
    'aldryn_apphooks_config',
    'aldryn_categories',
    'aldryn_common',
    'aldryn_newsblog',
    'aldryn_people',
    'aldryn_translation_tools',
    'appconf',
    'parler',
    'sortedm2m',
    'taggit',

    # my apps
    'tournament',
    'webpack_loader',
    'rd_django',
    'bycco'
)

LANGUAGE_CODE = 'nl'
LANGUAGES = (
    ## Customize this
    ('en', 'en'),
    ('nl', 'nl'),
    ('fr', 'fr'),
    ('de', 'de'),
)




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
        'tournament': {
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

PARTICIPANTS_ENABLED = 1

PRODUCTION = True

ROOT_URLCONF = 'bycco.urls'

SECRET_KEY = 'kustabitjevierkantigmekloten'

SITE_ID = 1

STATIC_ROOT = 'static'
STATIC_URL = '/static/'

SUBSCRIPTIONS_ENABLED = 1

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
                'rd_django.context_processor.tamplate_settings',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                'django.template.loaders.eggs.Loader'
            ],
        },
    },
]

TEMPLATE_SETTINGS = [
    'PRODUCTION', 'PARTICIPANTS_ENABLED', 'SUBSCRIPTIONS_ENABLED',
    'TOURNAMENT_ENABLED'
]

TIME_ZONE = 'Europe/Brussels'

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters'
)

TOURNAMENT_ENABLED = 0

USE_I18N = True

USE_L10N = True

USE_TZ = True

WSGI_APPLICATION = 'bycco.wsgi.application'

try:
    from local_settings import *
    print('local_settings read')
except ImportError:
    print('No local settings found')
