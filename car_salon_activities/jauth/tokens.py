"""
tokns.py: File, containing implementation of JWT token for a jauth app.
"""


from __future__ import annotations
import logging
from typing import ClassVar
from jauth.models import User
from jauth.backends import TokenBackend


logger = logging.getLogger(__name__)


class Token:
    """
    Token: Custom JWT token class, that provides actions with jwt token.
    """

    backend_class: ClassVar[type[TokenBackend]] = TokenBackend

    def __init__(self, *, token: str, type: str) -> None:
        """
        __init__: Instantiates Token instance.
        Args:
            token (str): Token value.
            type (str): Token type.
        """

        self.token: str = token
        self.type: str = type
        self.expired: bool = False
        self.invalid: bool = False

    @classmethod
    def for_user(cls, user: User) -> tuple[Token, Token]:
        """
        for_user: Generates and returns new pair of token: access and refresh.

        Args:
            user (User): User instance.

        Returns:
            tuple[Token, Token]: New pair of token: access and refresh.
        """

        access_token: str = cls.backend_class.generate_token(type='access', user_id=user.id)
        refresh_token: str = cls.backend_class.generate_token(type='refresh', user_id=user.id)
        return cls(token=access_token, type='access'), cls(token=refresh_token, type='refresh')

    def get_user_by_token(self) -> User:
        """
        get_user_by_token: Returns user according to token.

        Raises:
            Exception: Raises when verify method is not called.

        Returns:
            User: User instance.
        """

        if not hasattr(self, '_payload'):
            logger.error('Function get_user_by_token called before verify.')
            raise Exception('You must call verify before any action with token.')

        user_id: int = self._payload.get('sub', None)

        if user_id is None:
            return None

        user: User = User.objects.filter(pk=user_id).first()

        return user

    def verify(self) -> bool:
        """
        verify: Verifies if token is valid.

        Returns:
            bool: True if valid False if invalid.
        """

        try:
            self._payload: dict = self.backend_class.get_payload_by_token(token=self.token)
            return True
        except self.backend_class.token_expired_error:
            self.expired = True
        except self.backend_class.token_invalid_error:
            self.invalid = True

        return False
