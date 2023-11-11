"""
test_services.py: File, containing unit tests for jauth.services.
"""


import pytest
from jauth.tasks import send_confirmation_mail
from jauth.models import User
from jauth.tokens import Token
from jauth.services import UserService


class TestUserService:
    @pytest.fixture(scope='function', autouse=True)
    def user_service(self):
        self.service = UserService()

    def test_send_confirmation_link(self, user, mocker):
        mock = mocker.MagicMock(return_value=user)
        mocker.patch.object(User.objects, 'get', mock)

        mock = mocker.MagicMock()
        mocker.patch.object(send_confirmation_mail, 'delay', mock)

        self.service.send_confirmation_link(user.email)

        mock.assert_called_once()

    def test_send_reset_password_link(self, user, mocker):
        mock = mocker.MagicMock(return_value=user)
        mocker.patch.object(User.objects, 'get', mock)

        mock = mocker.MagicMock()
        mocker.patch.object(send_confirmation_mail, 'delay', mock)

        self.service.send_reset_password_link(user.email)

        mock.assert_called_once()

    def test_get_user_by_token(self, user, mocker):
        mock = mocker.MagicMock(return_value=None)
        mocker.patch.object(Token, 'verify', mock)

        assert self.service.get_user_by_token('token') is None

        mock = mocker.MagicMock(return_value=True)
        mocker.patch.object(Token, 'verify', mock)
        mock = mocker.MagicMock(return_value=user)
        mocker.patch.object(Token, 'get_user_by_token', mock)

        assert user == self.service.get_user_by_token('token')

    def test_set_user_as_inactive(self, user):
        user.is_active = True
        self.service.set_user_as_inactive(user)

        assert user.is_active is False

    def test_set_user_as_not_verified(self, user):
        user.is_verified = True
        self.service.set_user_as_not_verified(user)

        assert user.is_verified is False

    def test_set_user_as_verified(self, user):
        user.is_verified = False
        self.service.set_user_as_verified(user)

        assert user.is_verified is True

    def test_get_user_by_email(self, user, mocker):
        mock = mocker.MagicMock(return_value=User.objects)
        mocker.patch.object(User.objects, 'filter', mock)

        mock = mocker.MagicMock(return_value=user)
        mocker.patch.object(User.objects, 'first', mock)

        assert self.service.get_user_by_email(user.email) == user
