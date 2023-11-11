"""
conftest.py: File, containing common fixtures for integration tests.
"""


import os
import pytest
from django.conf import settings
from rest_framework.test import APIClient


@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES['default'] = {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('DB_NAME'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'ATOMIC_REQUESTS': True,
        'CONN_MAX_AGE': 0,
    }


@pytest.fixture(scope='function')
def client():
    return APIClient()
