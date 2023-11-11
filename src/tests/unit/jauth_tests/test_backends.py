"""
test_backends.py: File, containing unit tests for jauth.backends.
"""


import pytest
from jauth.backends import TokenBackend


class TestTokenBackend:
    @pytest.fixture(scope='function', autouse=True)
    def token_backend(self):
        self.token_backend = TokenBackend()

    def test_generate_token(self):
        access_token = self.token_backend.generate_token(type='access', user_id=1)

        assert isinstance(access_token, str)

        refresh_token = self.token_backend.generate_token(type='refresh', user_id=1)

        assert isinstance(refresh_token, str)

        with pytest.raises(ValueError):
            self.token_backend.generate_token(type='unknown', user_id=1)

    def test_get_payload_by_token(self):
        access_token = self.token_backend.generate_token(type='access', user_id=1)
        payload = self.token_backend.get_payload_by_token(token=access_token)

        assert isinstance(payload, dict)
