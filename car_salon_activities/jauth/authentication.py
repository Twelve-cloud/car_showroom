"""
authentification.py: File, containing implementation of JWT authentication for a jauth app.
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
        AuthenticationFailed: Raises when token is invalid.
        AuthenticationFailed: Raises when token is not correct.
    """

    token_class: ClassVar[type[Token]] = Token
    www_authenticate_realm: ClassVar[str] = 'api'
    www_authenticate_error: ClassVar[str] = 'invalid_token'

    def authenticate(self, request: Request) -> tuple[User, Token]:
        """
        authenticate: Provides authentication of request.

        Args:
            request (Request): Request instance.

        Raises:
            AuthenticationFailed: Raises when token structure is not correct.
            AuthenticationFailed: Raises when token type is not correct.
            AuthenticationFailed: Raises when token is expired.
            AuthenticationFailed: Raises when token is invalid.
            AuthenticationFailed: Raises when token is not correct.

        Returns:
            tuple[User, Token]: Tuple with access token and refresh token.
        """

        header = self.get_header(request)

        if header is None:
            return None

        token_type, access_token = self.get_token(header)

        if token_type is None or access_token is None:
            raise AuthenticationFailed('Token structure is not correct.')

        is_correct = self.check_if_token_type_is_correct(token_type)

        if not is_correct:
            raise AuthenticationFailed('Token type is not correct.')

        token = self.token_class(token=access_token, type='access')

        is_verified = token.verify()

        if not is_verified:
            if token.expired:
                raise AuthenticationFailed('Token is expired.')

            if token.invalid:
                raise AuthenticationFailed('Token is invalid.')

        user = token.get_user_by_token()

        if user is None:
            raise AuthenticationFailed('Token is not correct.')

        return user, token

    def authenticate_header(self, request: Request) -> str:
        """
        authenticate_header: Returns value of WWW-Authenticate header.

        Args:
            request (Request): Request instance.

        Returns:
            str: String that specify how to authenticate.
        """

        return f'Bearer="{self.www_authenticate_error}" realm="{self.www_authenticate_realm}"'

    def get_header(self, request: Request) -> str:
        """
        get_header: Returns value of Authorization header.

        Args:
            request (Request): Request instance.

        Returns:
            str: Value of Authorization header.
        """

        header = request.META.get(settings.JWT_TOKEN['HEADER_NAME'], None)
        return header

    def get_token(self, header: str) -> tuple[Optional[str], Optional[str]]:
        """
        get_token: Returns access token type and access token value.

        Args:
            header (str): Value of Authorization header.

        Returns:
            tuple[Optional[str], Optional[str]]: Token type and token value.
        """

        try:
            token_type, access_token = header.split()
            return token_type, access_token
        except Exception:
            return None, None

    def check_if_token_type_is_correct(self, token_type: str) -> bool:
        """
        check_if_token_type_is_correct: Checks if token type is correct according to settings.

        Args:
            token_type (str): Type of the token.

        Returns:
            bool: Value that shows if token type is correct.
        """

        return False if token_type != settings.JWT_TOKEN['TOKEN_TYPE'] else True
