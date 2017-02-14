from .base import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'TEST_SECRET_KEY'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
