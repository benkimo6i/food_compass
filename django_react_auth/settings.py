"""
Django settings for django_react_auth project.

Generated by 'django-admin startproject' using Django 1.9.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@g$7kxw@0uq0k*u^cyga^y6)@#ro@2y6dve+y#=2r3-whw@p*7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #third-party apps
    'rest_framework',
    'rest_framework.authtoken',
    'storages',
    #internal apps
    'api'
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_react_auth.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_react_auth.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'food_compass',
        'USER': 'food_compass_user',
        'PASSWORD': 'Briar718!',
        'HOST': 'localhost',
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
if DEBUG:

    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, "staticfiles", "media")

    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'assets'),
    )

if not DEBUG:
    import dj_database_url
    PREPEND_URL = "sleepy-anchorage-76452.herokuapp.com/"


    DATABASES['default'] =  dj_database_url.config()

    # Honor the 'X-Forwarded-Proto' header for request.is_secure()
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    # Allow all host headers
    ALLOWED_HOSTS = ['*']

    AWS_STORAGE_BUCKET_NAME = 'foodcompass'
    AWS_ACCESS_KEY_ID = 'AKIAIWWPYMRO7FTYHTPA'
    AWS_SECRET_ACCESS_KEY = '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'
    # Tell django-storages that when coming up with the URL for an item in S3 storage, keep
    # it simple - just use this domain plus the path. (If this isn't set, things get complicated).
    # This controls how the `static` template tag from `staticfiles` gets expanded, if you're using it.
    # We also use it in the next setting.
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'assets'),
    )

    # This is used by the `static` template tag from `static`, if you're using that. Or if anything else
    # refers directly to STATIC_URL. So it's safest to always set it.
    STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN

    # Tell the staticfiles app to use S3Boto storage when writing the collected static files (when
    # you run `collectstatic`).
    # STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

    STATICFILES_LOCATION = 'static'
    STATICFILES_STORAGE = 'django_react_auth.custom_storages.StaticStorage'
    STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)

    MEDIAFILES_LOCATION = 'media'
    MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
    DEFAULT_FILE_STORAGE = 'django_react_auth.custom_storages.MediaStorage'



