from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Application definition
INSTALLED_APPS += [
    'debug_toolbar'
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]

ROOT_URLCONF = 'vocationQA.urls.local'

INTERNAL_IPS = ['127.0.0.1']