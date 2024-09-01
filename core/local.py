from .base import *
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
    # 'default': {
    #     "ENGINE": "django.db.backends.postgresql",
    #     "NAME": env('POSTGRES_DB'),
    #     "USER": env('POSTGRES_USER'),
    #     "PASSWORD": env('POSTGRES_PASSWORD'),
    #     "HOST": env('POSTGRES_HOST'),
    #     "PORT": 5432,
    # }
}

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
