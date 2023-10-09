"""
tokns.py: File, containing implementation of JWT token for a jauth app.
"""


from __future__ import annotations
from typing import ClassVar, Optional
from jauth.models import User
from jauth.backends import TokenBackend


class Token:
    """
    Token: Custom JWT token class, that provides actions with jwt token.
    """

    backend_class: ClassVar[type[TokenBackend]] = TokenBackend

    def __init__(self, *, token: str, type: str) -> None:
        self.token: str = token
        self.type: str = type
        self.expired: bool = False
        self.invalid: bool = False

    @classmethod
    def for_user(cls, user: User) -> tuple[Token, Token]:
        access_token = cls.backend_class.generate_token(type='access', user_id=user.id)
        refresh_token = cls.backend_class.generate_token(type='refresh', user_id=user.id)
        return cls(token=access_token, type='access'), cls(token=refresh_token, type='refresh')

    def get_user_by_token(self) -> User:
        if not hasattr(self, '_payload'):
            raise Exception('You must call verify before any action with token.')

        user_id: int = self._payload.get('sub', None)

        if user_id is None:
            return None

        user: User = User.objects.filter(pk=user_id).first()

        return user

    def verify(self) -> Optional[bool]:
        try:
            self._payload: dict = self.backend_class.get_payload_by_token(token=self.token)
            return True
        except self.backend_class.token_expired_error:
            self.expired = True
        except self.backend_class.token_invalid_error:
            self.invalid = True

        return False
