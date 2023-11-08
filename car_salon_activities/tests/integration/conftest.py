import logging
import pytest
import sentry_sdk
from django.conf import settings
from rest_framework.test import APIClient


@pytest.fixture(scope='session', autouse=True)
def disable_sentry():
    sentry_sdk.init()


@pytest.fixture(scope='session', autouse=True)
def disable_logging():
    logging.disable(logging.CRITICAL)


@pytest.fixture(scope='session', autouse=True)
def django_db_settings():
    settings.DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "testbase",
        "ATOMIC_REQUESTS": True,
    }


@pytest.fixture(scope='function')
def client():
    return APIClient()
