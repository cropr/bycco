import os
from YamJam import yamjam

gettext = lambda s: s
_ = lambda s:s
cfg = yamjam().get('bycco') or {}


ALLOWED_HOSTS = cfg.get('allowed_hosts', [])

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
    ('page.html', 'Page'),
    ('landing.html', 'Landing page')
)

CMS_PERMISSION = True

CMS_PLACEHOLDER_CONF = {}

DATA_DIR = os.path.dirname(os.path.dirname(__file__))

dbcfg = cfg.get('db') or {}
DATABASES = {
    'default': {
        'ENGINE': dbcfg.get('engine',  'django.db.backends.postgresql_psycopg2'),
        'HOST': dbcfg.get('host', 'localhost'),
        'NAME': 'bycco',
        'PASSWORD': dbcfg.get('password'),
        'PORT': dbcfg.get('port', ''),
        'USER': dbcfg.get('user'),
    },
}

DEBUG = cfg.get('debug', True)

EMAIL_HOST = cfg.get('email_host', 'localhost')
EMAIL_PORT = cfg.get('email_port', 1025)

INSTALLED_APPS = (
    'djangocms_admin_style',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'cms',
    'menus',
    'sekizai',
    'treebeard',
    'djangocms_text_ckeditor',
    'filer',
    'easy_thumbnails',
    'djangocms_column',
    'djangocms_link',
    'cmsplugin_filer_file',
    'cmsplugin_filer_folder',
    'cmsplugin_filer_image',
    'cmsplugin_filer_utils',
    'djangocms_style',
    'djangocms_snippet',
    'djangocms_googlemap',
    'djangocms_video',
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
        'django' : {
            'level': 'INFO',
            'handlers': ['console'],
        }
    },
}


MEDIA_ROOT = cfg.get('media_root', os.path.join(DATA_DIR, 'media'))
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

PARLER_LANGUAGES = {
    1: (
        {'code': 'nl',},
        {'code': 'en',},
        {'code': 'fr', },
        {'code': 'de', },
    ),
    'default': {
        'fallbacks': ['nl', 'fr', 'de'],
    }
}

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': [],
#     'DEFAULT_PERMISSION_CLASSES': [],
# }

ROOT_URLCONF = 'bycco.urls'

SECRET_KEY = 'kustabitjevierkantigmekloten'

SITE_ID = 1

STATIC_ROOT = cfg.get('static_root')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'fe_dist', 'static'),
)

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
                'cms.context_processors.cms_settings'
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
