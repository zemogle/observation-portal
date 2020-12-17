"""
Django settings for observation_portal project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from lcogt_logging import LCOGTFormatter

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', '2xou30pi2va&ed@n2l79n807k%@szj1+^uj&)y09_w62eji!m^')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', False)

ALLOWED_HOSTS = ['observation-portal-dev.lco.global', '*']

ADMINS = [
    ('Softies', 'softies@lco.global')
]

SITE_ID = 1
ACCOUNT_ACTIVATION_DAYS = 7

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',
    'registration',  # must come before admin to use custom templates
    'django.contrib.admin',
    'rest_framework',
    'drf_yasg',
    'django_filters',
    'rest_framework.authtoken',
    'bootstrap4',
    'oauth2_provider',
    'corsheaders',
    'django_extensions',
    'django_dramatiq',
    'observation_portal.accounts.apps.AccountsConfig',
    'observation_portal.requestgroups.apps.RequestGroupsConfig',
    'observation_portal.observations.apps.ObservationsConfig',
    'observation_portal.proposals.apps.ProposalsConfig',
    'observation_portal.sciapplications.apps.SciapplicationsConfig',
]

MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'observation_portal.common.middleware.RequestLogMiddleware',
]

ROOT_URLCONF = 'observation_portal.urls'

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

WSGI_APPLICATION = 'observation_portal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# https://www.postgresql.org/docs/9.6/runtime-config-client.html#GUC-IDLE-IN-TRANSACTION-SESSION-TIMEOUT
PORTAL_IDLE_IN_TRANSACTION_TIMEOUT = 60 * 60 * 1000  # 1 hour

DATABASES = {
   'default': {
       'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql'),
       'NAME': os.getenv('DB_NAME', 'observation_portal'),
       'USER': os.getenv('DB_USER', 'postgres'),
       'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
       'HOST': os.getenv('DB_HOST', '127.0.0.1'),
       'PORT': os.getenv('DB_PORT', '5432'),
       'OPTIONS': {
           'options': f'-c idle_in_transaction_session_timeout={PORTAL_IDLE_IN_TRANSACTION_TIMEOUT}'
       }
   }
}

OAUTH2_PROVIDER_ACCESS_TOKEN_MODEL = 'oauth2_provider.AccessToken'
OAUTH2_PROVIDER_APPLICATION_MODEL = 'oauth2_provider.Application'
OAUTH2_PROVIDER_REFRESH_TOKEN_MODEL = 'oauth2_provider.RefreshToken'
MIGRATION_MODULES = {
    'oauth2_provider': 'observation_portal.accounts.oauth2_migrations'
}

CACHES = {
     'default': {
         'BACKEND': os.getenv('CACHE_BACKEND', 'django.core.cache.backends.locmem.LocMemCache'),
         'LOCATION': os.getenv('CACHE_LOCATION', 'unique-snowflake')
     },
     'locmem': {
         'BACKEND': os.getenv('LOCAL_CACHE_BACKEND', 'django.core.cache.backends.locmem.LocMemCache'),
         'LOCATION': 'locmem-cache'
     }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = [
    'observation_portal.accounts.backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend',
    'oauth2_provider.backends.OAuth2Backend',
]

OAUTH2_PROVIDER = {
    'ACCESS_TOKEN_EXPIRE_SECONDS': 86400 * 30 * 24,  # 2 years
    'REFRESH_TOKEN_EXPIRE_SECONDS': 86400 * 30 * 24  # 2 years
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/(api|accounts|media)/.*$|^/o/.*'
LOGIN_REDIRECT_URL = '/accounts/loggedinstate/'

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = False

USE_TZ = True

DATETIME_FORMAT = 'Y-m-d H:i:s'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME', 'observation-portal-test-bucket')
AWS_S3_REGION_NAME = os.getenv('AWS_REGION', 'us-west-2')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', None)
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', None)
AWS_IS_GZIPPED = True
AWS_LOCATION = os.getenv('MEDIAFILES_DIR', 'media')
AWS_DEFAULT_ACL = None
AWS_S3_SIGNATURE_VERSION = 's3v4'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_URL = '/static/'
STATIC_ROOT = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATICFILES_STORAGE = os.getenv('STATIC_STORAGE', 'django.contrib.staticfiles.storage.StaticFilesStorage')
MEDIAFILES_DIR = os.getenv('MEDIAFILES_DIR', 'media')
MEDIA_URL = '' if AWS_ACCESS_KEY_ID else '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
DEFAULT_FILE_STORAGE = os.getenv('MEDIA_STORAGE', 'django.core.files.storage.FileSystemStorage')

EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_USE_TLS = True
EMAIL_HOST = os.getenv('EMAIL_HOST', 'localhost')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
EMAIL_PORT = os.getenv('EMAIL_PORT', 587)
DEFAULT_FROM_EMAIL = 'Webmaster <portal@lco.global>'
SERVER_EMAIL = DEFAULT_FROM_EMAIL

ELASTICSEARCH_URL = os.getenv('ELASTICSEARCH_URL', 'http://localhost')
CONFIGDB_URL = os.getenv('CONFIGDB_URL', 'http://localhost')
DOWNTIMEDB_URL = os.getenv('DOWNTIMEDB_URL', 'http://localhost')

REST_FRAMEWORK = {
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.ScopedRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'requestgroups.cancel': '2000/day',
        'requestgroups.create': '5000/day',
        'requestgroups.validate': '20000/day'
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            '()': LCOGTFormatter
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO'
        },
        'rise_set': {
            'level': 'WARNING'
        },
        'portal_request': {
            'level': 'INFO',
            'propogate': False
        }
    }
}

DRAMATIQ_BROKER = {
    "BROKER": "dramatiq.brokers.redis.RedisBroker",
    "OPTIONS": {
        "url": "redis://" + os.getenv("DRAMATIQ_BROKER_HOST", "redis") + ":" +
               str(os.getenv("DRAMATIQ_BROKER_PORT", 6379)),
    },
    "MIDDLEWARE": [
        "dramatiq.middleware.Prometheus",
        "dramatiq.middleware.AgeLimit",
        "dramatiq.middleware.TimeLimit",
        "dramatiq.middleware.Callbacks",
        "dramatiq.middleware.Retries",
        "django_dramatiq.middleware.DbConnectionsMiddleware",
    ]
}

TEST_RUNNER = 'observation_portal.test_runner.MyDiscoverRunner'

try:
    from local_settings import *  # noqa
except ImportError as e:
    pass

try:
    INSTALLED_APPS += LOCAL_INSTALLED_APPS  # noqa
    ALLOWED_HOSTS += LOCAL_ALLOWED_HOSTS  # noqa
except NameError:
    pass
