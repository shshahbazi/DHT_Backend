from .base import *

# TODO: Change this to false
DEBUG = True

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env('POSTGRES_DB'),
        "USER": env('POSTGRES_USER'),
        "PASSWORD": env('POSTGRES_PASSWORD'),
        "HOST": 'dhtdb',
        "PORT": '5432',
    }
}

# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
