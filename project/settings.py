import mongoengine
import sys
from os.path import abspath, dirname, join

from settings_local import *

sys.path.insert(0, '../..')
ROOT_PATH = abspath(dirname(__file__))
BASE_DIR = dirname(dirname(__file__))
SECRET_KEY = 'n7)u4v#=cbsvse!nf@lh1zv0qsoej!g$95eqkd(7irzr4zn7)5'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []


# Application definition
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'mongoengine.django.mongo_auth',
    'social.apps.django_app.default',
    'social.apps.django_app.me', # this is the line that fails
)
AUTHENTICATION_BACKENDS = (
    'mongoengine.django.auth.MongoEngineBackend',
    'django.contrib.auth.backends.ModelBackend',
    'social.backends.facebook.FacebookOAuth2',
)
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'project.urls'
WSGI_APPLICATION = 'project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.dummy'
    }
}

TEMPLATE_DIRS = (
    join(ROOT_PATH, 'templates'),
)

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

_MONGODB_HOST = 'localhost'
_MONGODB_NAME = 'test'
_MONGODB_DATABASE_HOST = \
    'mongodb://%s/%s' \
    % (_MONGODB_HOST, _MONGODB_NAME)

mongoengine.connect(_MONGODB_NAME, host=_MONGODB_DATABASE_HOST)

# Auth Stuff
SOCIAL_AUTH_STORAGE = 'social.apps.django_app.me.models.DjangoStorage'
SOCIAL_AUTH_FACEBOOK_KEY = '***'        #real stuf here
SOCIAL_AUTH_FACEBOOK_SECRET = '***'     #real stuf here
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email','user_location']