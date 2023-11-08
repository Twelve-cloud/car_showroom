"""
test_tokens.py: File, containing tests for jauth.tokens.
"""


import pytest
from jauth.models import User
from jauth.tokens import Token
from jauth.backends import TokenBackend


class TestToken:
    @pytest.fixture(scope='function', autouse=True)
    def tokens(self, user, mocker, settings):
        token = TokenBackend.generate_token(type='access', user_id=user.id)
        self.token = Token(token=token, type='access')

        self.invalid_token = Token(token='invalid', type='access')

        old_access_token_lifetime = settings.JWT_TOKEN['ACCESS_TOKEN_LIFETIME_MINUTES']
        settings.JWT_TOKEN['ACCESS_TOKEN_LIFETIME_MINUTES'] = 0

        token = TokenBackend.generate_token(type='access', user_id=user.id)

        settings.JWT_TOKEN['ACCESS_TOKEN_LIFETIME_MINUTES'] = old_access_token_lifetime
        self.expired_token = Token(token=token, type='access')

    def test_for_user(self, user):
        access_token, refresh_token = Token.for_user(user)

        assert isinstance(access_token, Token)
        assert access_token.type == 'access'

        assert isinstance(refresh_token, Token)
        assert refresh_token.type == 'refresh'

    def test_verify(self, user):
        assert self.token.verify() is True
        assert self.invalid_token.verify() is False
        assert self.expired_token.verify() is False

    def test_get_user_by_token(self, user, mocker):
        with pytest.raises(Exception):
            self.token.get_user_by_token()

        self.token.verify()

        mocker.patch.dict(self.token._payload, {}, clear=True)

        assert self.token.get_user_by_token() is None

        self.token.verify()

        mock = mocker.MagicMock(return_value=User.objects)
        mocker.patch.object(User.objects, 'filter', mock)

        mock = mocker.MagicMock(return_value=user)
        mocker.patch.object(User.objects, 'first', mock)

        assert self.token.get_user_by_token() == user
