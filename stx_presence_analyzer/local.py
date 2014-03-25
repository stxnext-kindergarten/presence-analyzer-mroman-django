from stx_presence_analyzer.settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR('db.sqlite3'),
    }
}

MEDIA_ROOT = BASE_DIR('public')