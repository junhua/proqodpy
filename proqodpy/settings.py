"""
Django settings for proqodpy project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+^ya-4eus4sv&idx!-*1lol+5!^eker-&i@75yc%h$l(8)h5u4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'authnz.ProqodUser'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party
    'corsheaders',

    # REST
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'django_filters',

    'authnz',
    'myapp.courses',
    'myapp.analytics',
    'myapp.submissions',

    'api.v1',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = [
    'api.proqod.com',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}

DJOSER = {
    # 'DOMAIN': 'cloud.proqod.com',
    'SITE_NAME': 'ProQod',
    'PASSWORD_RESET_CONFIRM_URL': 'auth/password/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': 'auth/activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
}

ROOT_URLCONF = 'proqodpy.urls'


STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# LIB_DIR = os.path.join(BASE_DIR, 'libs')
LOG_DIR = os.path.join(BASE_DIR, 'log')


# STATICFILES_DIRS = (
#    os.path.join(BASE_DIR, 'static'),
#)

ADMIN_MEDIA_PREFIX = '/static/admin'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
# LIB_URL = '/libs/'

FIXTURE_DIRS = (
    '/dev/data/',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),
                 os.path.join(BASE_DIR, 'templates/djoser'),
                 os.path.join(BASE_DIR, 'static/ngproject')
                 ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # 'django.template.context_processors.debug',
                # 'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'proqodpy.wsgi.application'

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'log/email')

import sys
LOGGING = {
    'version': 1,
    'disable_existing_loggers': 'True',
    'root': {
        'level': 'WARNING',
        'handlers': ['file'],
    },
    'filters': {
        # Only sends error when DEBUG is false
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(name)s %(module)s %(message)s'
        }
    },
    'handlers': {
        # Send all messages to console
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'verbose',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR + '/debug.log',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        #'sentry': {
        #    'level': 'WARNING',
        #    'class': 'raven.contrib.django.handlers.SentryHandler'
        #}
    },
    'loggers': {
        'django.request': {
            'handlers': ['console', 'file'],
            'level': 'ERROR',
            'propogate': False,
        },
        'django.db': {
            'handlers': ['console'],
            'level': 'ERROR',
        },
        'proqod': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG'
        }
    }
}


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'proqod',
    }
}


# Handle CORS: https://github.com/ottoyiu/django-cors-headers/

# CORS_ORIGIN_REGEX_WHITELIST = ('^(https?://)?(.*\.)?proqod\.com$', )

CORS_ORIGIN_ALLOW_ALL = True


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Singapore'

USE_I18N = True

USE_L10N = True

USE_TZ = True
