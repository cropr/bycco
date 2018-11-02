#    Copyright 2018 Ruben Decrop
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

print('loading local settings in dev environment')

import os, os.path

# config parameters
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

ALLOWED_HOSTS = ['*']

CHESSAPI_URL = 'http://localhost:8001/'

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'localhost',
        'NAME': 'bycco',
        'USER': '$$$user',
        'PASSWORD': '$$$password',
    }

}

EMAIL_HOST = '127.0.0.1'
EMAIL_PORT = 1025

OLDSITE = 'https://www.frbe-kbsb.be'

STATICFILES_DIRS = (
    os.path.join(ROOT_DIR, 'frontend', 'static'),
)

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'static/',
        'STATS_FILE': os.path.join(ROOT_DIR,  'frontend', 'webpack-stats.json'),
    }
}
