"""
user_auth_service.py: File, containg logic with authentication of the user.
"""


from typing import ClassVar, Optional
from dataclasses import dataclass
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound, PermissionDenied
from jauth.models import User
from jauth.tokens import Token


@dataclass
class CredentialsDTO:
    """
    CretentialsDTO: Credentials data transfer object.
    """

    email: str
    password: str


@dataclass
class TokenPairDTO:
    """
    TokenPairDTO: TokenPair data transfer object.
    """

    access: Optional[str] = None
    refresh: Optional[str] = None


class UserAuthService:
    """
    UserAuthService: UserAuthService class. It handles authentication actions like login.

    Raises:
        NotFound: User not found.
        PermissionDenied: Account is not verified.
        PermissionDenied: Token is expired.
        PermissionDenied: Token is invalid.
        PermissionDenied: Token is not correct.
    """

    model_class: ClassVar[type[User]] = User
    token_class: ClassVar[type[Token]] = Token

    def _prepare_credentials(self, dto: CredentialsDTO) -> dict[str, str]:
        """
        _prepare_credentials: Make credentials dict from CredentialsDTO.

        Args:
            dto (CredentialsDTO): CredentialsDTO.

        Returns:
            dict[str, str]: Credentials dict object.
        """

        return {
            'email': dto.email,
            'password': dto.password,
        }

    def _prepare_token_pair(self, dto: TokenPairDTO) -> dict[str, str]:
        """
        _prepare_token_pair: Make token pair dict from TokenPairDTO.

        Args:
            dto (TokenPairDTO): TokenPairDTO.

        Returns:
            dict[str, str]: Token pair dict object.
        """

        token_pair: dict[str, Optional[str]] = {
            'access': dto.access,
            'refresh': dto.refresh,
        }

        return {field: value for field, value in token_pair.items() if value}

    def _make_token_pair_dto(self, access: Token, refresh: Token) -> TokenPairDTO:
        """
        _make_token_pair_dto: Make TokenPairDTO from access and refresh params

        Args:
            access (Token): Token instance.
            refresh (Token): Token instance.

        Returns:
            TokenPairDTO: TokenPairDTO.
        """

        return TokenPairDTO(
            access=access.token,
            refresh=refresh.token,
        )

    def get_tokens(self, dto: CredentialsDTO) -> TokenPairDTO:
        """
        get_tokens: Return pair of tokens - access and refresh.

        Args:
            dto (CredentialsDTO): CredentialsDTO.

        Raises:
            NotFound: User is not found.
            PermissionDenied: Account is not verified.

        Returns:
            TokenPairDTO: TokenPairDTO.
        """

        credentials_data: dict[str, str] = self._prepare_credentials(dto)

        user: User = get_object_or_404(self.model_class, email=credentials_data['email'])

        if not user.check_password(credentials_data['password']):
            raise NotFound(
                detail='Password is not correct.',
            )

        if not user.is_active and not user.is_verified:
            raise PermissionDenied(
                detail='Account is not verified.',
            )

        if not user.is_active and user.is_verified:
            user.set_is_active(True)

        user.set_last_login()

        token_pair_dto: TokenPairDTO = self._make_token_pair_dto(*self.token_class.for_user(user))

        return token_pair_dto

    def refresh(self, dto: TokenPairDTO) -> TokenPairDTO:
        """
        refresh: Return new pair of token: access and refresh, when access token is expired.

        Args:
            dto (TokenPairDTO): TokenPairDTO.

        Raises:
            PermissionDenied: Token is expired.
            PermissionDenied: Token is invalid.
            PermissionDenied: Token is not correct.

        Returns:
            TokenPairDTO: TokenPairDTO.
        """

        token_data: dict[str, str] = self._prepare_token_pair(dto)
        token: Token = self.token_class(token=token_data['refresh'], type='refresh')

        is_verified: Optional[bool] = token.verify()

        if not is_verified:
            if token.expired:
                raise PermissionDenied(
                    detail='Token is expired.',
                )

            if token.invalid:
                raise PermissionDenied(
                    detail='Token is invalid.',
                )

        user: Optional[User] = token.get_user_by_token()

        if user is None:
            raise PermissionDenied(
                detail='Token is not correct.',
            )

        user.set_last_login()

        token_pair_dto: TokenPairDTO = self._make_token_pair_dto(*self.token_class.for_user(user))

        return token_pair_dto
