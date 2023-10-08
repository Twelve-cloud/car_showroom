"""
authentification.py: File, containing implementation of JWT authentication for an jauth app.
"""


from typing import ClassVar, Optional
from django.conf import settings
from rest_framework import authentication
from rest_framework.request import Request
from rest_framework.exceptions import AuthenticationFailed
from jauth.models import User
from jauth.tokens import Token


class JWTAuthentication(authentication.BaseAuthentication):
    """
    JWTAuthentication: Custom authentication class that provides JWT authentication.

    Args:
        authentication.BaseAuthentication (_type_): Builtin superclass for an JWTAuthentication.

    Raises:
        AuthenticationFailed: Raises when token structure is not correct.
        AuthenticationFailed: Raises when token type is not correct.
        AuthenticationFailed: Raises when token is expired.
        AuthenticationFailed: Raises when token is not correct.
    """

    token_class: ClassVar[type[Token]] = Token
    www_authenticate_realm: ClassVar[str] = 'api'

    def authenticate(self, request: Request) -> tuple[User, Token]:
        header = self.get_header(request)

        if header is None:
            return None

        token_type, access_token = self.get_token(header)

        if token_type is None or access_token is None:
            raise AuthenticationFailed('Token structure is incorrect.')

        is_correct = self.check_if_token_type_is_correct(token_type)

        if not is_correct:
            raise AuthenticationFailed('Token type is not correct.')

        token = self.token_class(token=access_token, type='access')

        is_expired = token.check_exp_date()

        if is_expired is True:
            raise AuthenticationFailed('Token is expired.')

        user = token.get_user_by_token()

        if user is None:
            raise AuthenticationFailed('Token is not correct.')

        return user, token

    def authenticate_header(self, request: Request) -> str:
        return f'JWT realm={self.www_authenticate_realm}'

    def get_header(self, request: Request) -> str:
        header = request.META.get(settings.JWT_TOKEN['HEADER_NAME'], None)
        return header

    def get_token(self, header: str) -> tuple[Optional[str], Optional[str]]:
        try:
            token_type, access_token = header.split()
            return token_type, access_token
        except Exception:
            return None, None

    def check_if_token_type_is_correct(self, token_type: str) -> bool:
        return False if token_type != settings.JWT_TOKEN['TOKEN_TYPE'] else True
