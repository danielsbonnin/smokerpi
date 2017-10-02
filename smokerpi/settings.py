import os
import logging
import logging.config
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGGING = {
    'version': 1,
    'handlers': {
        'troubleshooting': {    
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'troubleshooting.log'),
            'maxBytes': 1024*1024*15,
            'backupCount': 10,
            },
        'thermometers': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'thermometers.log'),
            'maxBytes': 1024*1024*15,
            'backupCount': 10,
            },
        'pid': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'pid.log'),
            'maxBytes': 1024*1024*15,
            'backupCount': 10,
            },
        'heater': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'heater.log'),
            'maxBytes': 1024*1024*15,
            'backupCount': 10,
            },
        },
    'loggers': {
        'thermometers': {
            'handlers': ['thermometers', 'troubleshooting'],
            'level': 'INFO',
            'propagate': True,
            },
        'pid': {
            'handlers': ['pid', 'troubleshooting'],
            'level': 'INFO',
            'propagate': True,
            },
        'heater': {
            'handlers': ['heater', 'troubleshooting'],
            'level': 'INFO',
            'propagate': True,
            },
        }
    }
logging.config.dictConfig(LOGGING)
