from .local import *


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get("VOCATION_DB_NAME"),
        'HOST': os.environ.get("VOCATION_DB_HOST"),
        'PORT': os.environ.get("VOCATION_DB_PORT"),
        'USER': os.environ.get("VOCATION_DB_USER"),
        'PASSWORD': os.environ.get("VOCATION_DB_PASSWORD"),
        'ATOMIC_REQUESTS': True,
    }
}