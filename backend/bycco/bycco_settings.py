#    Copyright 2019 Chessdevil Consulting
#    Copyright 2019 Chessdevil Consulting

import os

MONGO_URL = 'mongodb://localhost:27017/'
MONGO_DB = 'bycco'

EMAIL= {
  'backend': 'SMTP',
  'host': 'localhost',
  'port': '1025',
  'sender': 'ruben.decrop@bycco.be',
  'bcc': 'registration@bycco.be',
}

LOG_CONFIG = {
    'version': 1,
    'formatters': {
        'simple': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
        'color': {
            'format':
            '%(log_color)s%(levelname)s%(reset)s: %(asctime)s %(bold)s%(name)s%(reset)s %(message)s',
            '()': 'reddevil.common.colorlogfactory.c_factory',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'color',
            'stream': 'ext://sys.stderr'
        }
    },
    'loggers': {
        'bycco': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'reddevil': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'fastapi': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'uvicorn': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}

INVOICENUMBERSTART = 1

GOOGLE_CLIENT_ID = '138759213444-sitmoe4qtoh3o2ust5vg5mtqe147spn6.apps.googleusercontent.com'
GOOGLE_LOGIN_DOMAINS = ['bycco.be']

TOKEN = {
    "timeout":  180,    # timeout in minutes
    "secret": "Ramskappelle",
    "algorithm": "HS256",
    "nocheck": True,
}

try:
    from local_settings import *
    print('local settings loaded')
except ImportError:
    print('No local settings found')
