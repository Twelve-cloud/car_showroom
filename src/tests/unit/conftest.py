"""
conftest.py: File, containing common fixtures for unit tests.
"""


import logging
import pytest
import sentry_sdk
from django.conf import settings
from core.models import CarModel
from jauth.models import User
from customer.models import CustomerModel
from showroom.models import ShowroomModel
from supplier.models import SupplierModel


@pytest.fixture(scope='session', autouse=True)
def update_settings():
    settings.SECRET_KEY = 'test_key'
    settings.FRONTEND_URL = 'test_frontend_url'


@pytest.fixture(scope='session', autouse=True)
def disable_sentry():
    sentry_sdk.init()


@pytest.fixture(scope='session', autouse=True)
def disable_logging():
    logging.disable(logging.CRITICAL)


@pytest.fixture(scope='function', autouse=True)
def no_save(mocker):
    for model in [User, CustomerModel, SupplierModel, ShowroomModel, CarModel]:
        mocker.patch.object(model, 'save', mocker.MagicMock())


@pytest.fixture(scope='function')
def user(mocker):
    return User(
        id=1,
        username='username1',
        password='password1',
        email='email1@mail.com',
        first_name='user_name',
        last_name='user_surname',
    )
