"""
Django settings for car_salon_activities project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""


import os
from typing import Optional
from pathlib import Path
import sentry_sdk
from celery.schedules import crontab


# -------------------------- SETRY SETTINGS -----------------------------------

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DNS'),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

# -------------------------- MAIN SETTINGS ------------------------------------

BASE_DIR: Path = Path(__file__).resolve().parent.parent

SECRET_KEY: Optional[str] = os.getenv('SECRET_KEY')

DEBUG: bool = os.getenv('DEBUG') == 'True'

ALLOWED_HOSTS: Optional[list] = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')

DEFAULT_CHARSET: str = 'utf8'

ROOT_URLCONF: str = 'config.urls'

AUTH_USER_MODEL: str = 'jauth.User'

# -------------------------- INSTALLED APPS -----------------------------------

DJANGO_APPS: list = [
    'django.contrib.staticfiles',
]

LOCAL_APPS: list = [
    'jauth.apps.JauthConfig',
    'core.apps.CoreConfig',
    'customer.apps.CustomerConfig',
    'showroom.apps.ShowroomConfig',
    'supplier.apps.SupplierConfig',
]

THIRD_PARTY_APPS: list = [
    'rest_framework',
    'django_filters',
    'drf_spectacular',
]

INSTALLED_APPS: list = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS

# -------------------------- MIDDLEWARES --------------------------------------

MIDDLEWARE: list = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ---------------------------- DATABASES --------------------------------------

DATABASES: dict = {
    'master': {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('DB_NAME'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'CONN_MAX_AGE': 0,
    },
    'default': {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('DB_NAME'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'CONN_MAX_AGE': 0,
    },
}

# ---------------------------- TEMPLATE SETTINGS -------------------------------

TEMPLATES: list = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
    }
]

# --------------------------- STATIC SETTINGS ----------------------------------

STATIC_URL: str = "/static/"

# ------------------------- LANGUAGE SETTINGS ---------------------------------

LANGUAGE_CODE: str = 'en-us'

USE_I18N: bool = False

USE_L10N: bool = False

TIME_ZONE: str = 'Europe/Minsk'

USE_TZ: bool = True

# ----------------------- DJANGO EMAIL SETTINGS -------------------------------

EMAIL_BACKEND: Optional[str] = os.getenv('EMAIL_BACKEND')

DEFAULT_FROM_EMAIL: Optional[str] = os.getenv('DEFAULT_FROM_EMAIL')

EMAIL_HOST: Optional[str] = os.getenv('EMAIL_HOST')

EMAIL_PORT: Optional[str] = os.getenv('EMAIL_PORT')

EMAIL_HOST_USER: Optional[str] = os.getenv('EMAIL_HOST_USER')

EMAIL_HOST_PASSWORD: Optional[str] = os.getenv('EMAIL_HOST_PASSWORD')

EMAIL_DEF_USER: Optional[str] = os.getenv('EMAIL_DEF_USER')

EMAIL_USE_TLS: bool = True

EMAIL_USE_SSL: bool = False

EMAIL_USE_LOCALTIME: bool = False

EMAIL_TIMEOUT: None = None

# -------------------------- LOGGING SETTINGS ---------------------------------

LOGGING: dict = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'short': {
            'format': '[%(asctime)s] %(levelname)s: %(message)s',
            'datefmt': '%Y.%m.%d %H:%M:%S',
        },
        'long': {
            'format': '[%(asctime)s][%(pathname)s; line: %(lineno)s] %(levelname)s: %(message)s',
            'datefmt': '%Y.%m.%d %H:%M:%S',
        },
    },
    'handlers': {
        'console_dev': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'short',
            'filters': ['require_debug_true'],
        },
        'console_prd': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'short',
            'filters': ['require_debug_false'],
        },
        'mail_prd': {
            'level': 'ERROR',
            'class': 'logging.handlers.SMTPHandler',
            'mailhost': EMAIL_HOST,
            'fromaddr': EMAIL_HOST_USER,
            'toaddrs': EMAIL_DEF_USER,
            'subject': 'ERROR in code',
            'credentials': (EMAIL_HOST_USER, EMAIL_HOST_PASSWORD),
            'secure': (),
            'formatter': 'short',
            'filters': ['require_debug_false'],
        },
        'console_dev_long': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'long',
            'filters': ['require_debug_true'],
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console_dev', 'console_prd'],
            'level': 'INFO',
        },
        'django.db.backends': {
            'handlers': ['console_dev', 'console_prd', 'mail_prd'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['mail_prd'],
            'level': 'WARNING',
            'propagate': True,
        },
        'jauth': {
            'handlers': ['console_dev_long', 'console_prd', 'mail_prd'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# --------------------------- DRF SETTINGS ------------------------------------

REST_FRAMEWORK: dict = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'jauth.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_PAGINATION_CLASS': 'config.paginators.CustomCursorPagination',
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_METADATA_CLASS': 'rest_framework.metadata.SimpleMetadata',
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'UNAUTHENTICATED_USER': None,
    'UNAUTHENTICATED_TOKEN': None,
    'UNICODE_JSON': False,
    'COMPACT_JSON': False,
    'STRICT_JSON': True,
}

# ------------------------ SPECTACULAR SETTINGS -------------------------------

SPECTACULAR_SETTINGS = {
    'TITLE': 'Can Salon Activities API',
    'DESCRIPTION': 'Modeling work of Car Showroom',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# -------------------------- JWT SETTINGS -------------------------------------

JWT_TOKEN: dict = {
    'ACCESS_TOKEN_LIFETIME_MINUTES': 1500,
    'REFRESH_TOKEN_LIFETIME_DAYS': 30,
    'TOKEN_TYPE': 'Bearer',
    'ENCODE_ALG': 'HS256',
    'DECODE_ALGS': ['HS256'],
    'HEADER_NAME': 'HTTP_AUTHORIZATION',
}

# ------------------------ RABBITMQ SETTINGS -----------------------------------

RABBITMQ: dict = {
    'PROTOCOL': 'amqp',
    'HOST': os.getenv('RABBITMQ_HOST'),
    'PORT': os.getenv('RABBITMQ_PORT'),
    'USER': os.getenv('RABBITMQ_USER'),
    'PASS': os.getenv('RABBITMQ_PASS'),
}

# ------------------------- REDIS SETTINGS -------------------------------------

REDIS: dict = {
    'PROTOCOL': 'redis',
    'HOST': os.getenv('REDIS_HOST'),
    'PORT': os.getenv('REDIS_PORT'),
    'PASS': os.getenv('REDIS_PASSWORD'),
    'DATABASE_NUMBER': os.getenv('REDIS_DB_NUMBER'),
}

# ------------------------- CELERY SETTINGS ------------------------------------

CELERY_ENABLE_UTC: bool = True

CELERY_TIMEZONE: str = 'Europe/Minsk'

CELERY_BROKER_URL: str = (
    f"{RABBITMQ['PROTOCOL']}://{RABBITMQ['USER']}:"
    f"{RABBITMQ['PASS']}@{RABBITMQ['HOST']}:{RABBITMQ['PORT']}"
)

CELERY_BROKER_TRANSPORT_OPTIONS: dict = {'visibility_timeout': 3600}

CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP: bool = True

CELERY_BROKER_CONNECTION_MAX_RETRIES: int = 200

CELERY_BROKER_USE_SSL: bool = False

CELERY_RESULT_BACKEND: str = (
    f"{REDIS['PROTOCOL']}://:{REDIS['PASS']}@"
    f"{REDIS['HOST']}:{REDIS['PORT']}/{REDIS['DATABASE_NUMBER']}"
)

CELERY_RESULT_BACKEND_TRANSPORT_OPTIONS: dict = {'visibility_timeout': 3600}

CELERY_RESULT_CACHE_MAX: bool = False

CELERY_REDIS_BACKEND_HEALTH_CHECK_INTERVAL: None = None

CELERY_REDIS_BACKEND_USE_SSL: bool = False

CELERY_BEAT_SCHEDULE: dict = {
    'clear-every-day': {
        'task': 'jauth.tasks.clear_database_from_waste_accounts',
        'schedule': crontab(minute=0, hour=0),
    },
    'delete_discounts_every_minute': {
        'task': 'core.tasks.delete_finished_discounts',
        'schedule': crontab(minute='*'),
    },
    'check_suppliers_every_hour': {
        'task': 'core.tasks.check_suppliers',
        'schedule': crontab(hour=0),
    },
    'buy_supplier_cars_every_ten_minutes': {
        'task': 'core.tasks.buy_supplier_cars',
        'schedule': crontab(minute='*/10'),
    },
}

# ---------------------- DJANGO DEBUG TOOLBAR SETTINGS -------------------------

if DEBUG:
    INSTALLED_APPS += [
        'debug_toolbar',
        'sslserver',
    ]

    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

    DEBUG_TOOLBAR_CONFIG: dict = {
        'SHOW_TOOLBAR_CALLBACK': lambda _request: True,
    }

    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] += [
        'rest_framework.renderers.BrowsableAPIRenderer',
    ]

    REST_FRAMEWORK['DEFAULT_PARSER_CLASSES'] += [
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ]

# -------------------------- OTHER SETTINGS ------------------------------------

WSGI_APPLICATION: str = 'config.wsgi.application'

DEFAULT_AUTO_FIELD: str = 'django.db.models.BigAutoField'

FRONTEND_URL: Optional[str] = os.getenv('FRONTEND_URL')
