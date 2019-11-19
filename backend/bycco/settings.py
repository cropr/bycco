from bycco.util.dataclassjson import DataclassEncoder

LOG_CONFIG = {
    'version': 1,
    'formatters': {
        'simple': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'simple',
            'stream': 'ext://sys.stderr'
        }
    },
    'loggers': {
        'bycco': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'flask': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'flask': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}

MONGODB = {
    'database': 'bycco'
}

RESTFUL_JSON = {'cls': DataclassEncoder}
