"""
Django settings for django_proj project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#h!i8uo+@jj=6r)*x603@2-7jlu85oq9-o$nhbu2so_@&0e4k6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# BEGIN SALT ALLOWED HOSTS(current used if not provisioned by salt)
ALLOWED_HOSTS = ['127.0.0.1']
# END SALT ALLOWED HOSTS


# Application definition

INSTALLED_APPS = [
    'django_nose',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_proj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'django_proj.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'mfserver2',
        'USER': 'mfserver2',
        'PASSWORD': 'mfserver2',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'django_log': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 25 * 1024 * 1024,
            'backupCount': 5,
            'filename': '/var/log/mfserver2/django.log',
        },
        'django_db_log': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 25 * 1024 * 1024,
            'backupCount': 5,
            'filename': '/var/log/mfserver2/django_db.log',
        },
        'django_request_log': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 25 * 1024 * 1024,
            'backupCount': 5,
            'filename': '/var/log/mfserver2/django_request.log',
        },
        'mfserver2_log': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 25 * 1024 * 1024,
            'backupCount': 5,
            'filename': '/var/log/mfserver2/mfserver2.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['django_log'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.db': {
            'handlers': ['django_db_log'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['django_request_log'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django_app': {
            'handlers': ['mfserver2_log'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
FIXTURE_DIRS = ('django_app/test/fixtures',)
