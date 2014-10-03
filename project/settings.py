import os
import mongoengine

<<<<<<< HEAD
from settings_local import *

=======
>>>>>>> b5a0f24f7291070596b1b9ba60e4760426254cde
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
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

<<<<<<< HEAD
=======

SOCIAL_AUTH_USER_MODEL = 'mongoengine.django.auth.User'

>>>>>>> b5a0f24f7291070596b1b9ba60e4760426254cde
# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.dummy'
    }
}

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

<<<<<<< HEAD
_MONGODB_HOST = 'localhost'
_MONGODB_NAME = 'test'
_MONGODB_DATABASE_HOST = \
    'mongodb://%s/%s' \
    % (_MONGODB_HOST, _MONGODB_NAME)
=======

SOCIAL_AUTH_USER_MODEL = 'mongoengine.django.auth.User'

_MONGODB_USER = '***'      #real stuf here
_MONGODB_PASSWD = '***'    #real stuf here
_MONGODB_HOST = '***'      #real stuf here
_MONGODB_NAME = '****'     #real stuf here
_MONGODB_DATABASE_HOST = \
    'mongodb://%s:%s@%s/%s' \
    % (_MONGODB_USER, _MONGODB_PASSWD, _MONGODB_HOST, _MONGODB_NAME)
>>>>>>> b5a0f24f7291070596b1b9ba60e4760426254cde

mongoengine.connect(_MONGODB_NAME, host=_MONGODB_DATABASE_HOST)

# Auth Stuff
SOCIAL_AUTH_STORAGE = 'social.apps.django_app.me.models.DjangoStorage'
SOCIAL_AUTH_FACEBOOK_KEY = '***'        #real stuf here
SOCIAL_AUTH_FACEBOOK_SECRET = '***'     #real stuf here
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email','user_location']