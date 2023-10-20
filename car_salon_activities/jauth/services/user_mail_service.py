"""
user_main_service.py: File, containing logic with sending mails.
"""


from typing import ClassVar, Optional
from dataclasses import dataclass
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ParseError
from jauth.tasks import send_confirmation_mail
from jauth.models import User
from jauth.tokens import Token


@dataclass
class EmailDTO:
    """
    EmailDTO: Email data transfer object.
    """

    email: str


@dataclass
class PasswordDTO:
    """
    PasswordDTO: Password data transfer object.
    """

    password: str


@dataclass
class ConfirmationTokenDTO:
    """
    ConfirmationTokenDTO: Confirmation data transfer object.
    """

    token: str


class UserMailService:
    """
    UserMailSerivce: UserMailService class. It handles sending email messages.

    Raises:
        ParseError: Bad token.
        ParseError: Bad token.
    """

    token_class: ClassVar[type[Token]] = Token
    model_class: ClassVar[type[User]] = User

    def _prepare_email(self, dto: EmailDTO) -> dict[str, str]:
        """
        _prepare_email: Make email dict from EmailDTO.

        Args:
            dto (EmailDTO): EmailDTO.

        Returns:
            dict[str, str]: Email dict object.
        """

        return {
            'email': dto.email,
        }

    def _prepare_password(self, dto: PasswordDTO) -> dict[str, str]:
        """
        _prepare_password: Make password dict from PasswordDTO.

        Args:
            dto (PasswordDTO): PasswordDTO.

        Returns:
            dict[str, str]: Password dict object.
        """

        return {
            'password': dto.password,
        }

    def _prepare_token(self, dto: ConfirmationTokenDTO) -> dict[str, str]:
        """
        _prepare_token: Make confirmation token dict from ConfirmationTokenDTO.

        Args:
            dto (ConfirmationTokenDTO): ConfirmationTokenDTO.

        Returns:
            dict[str, str]: Confirmation token dict object.
        """

        return {
            'token': dto.token,
        }

    def send_confirmation_link(self, dto: EmailDTO) -> None:
        """
        send_confirmation_link: Send confirmation link to email address.

        Args:
            dto (EmailDTO): EmailDTO.
        """

        mail_data: dict[str, str] = self._prepare_email(dto)
        user: User = self.model_class.objects.get(**mail_data)
        confirmation_token, _ = self.token_class.for_user(user)
        confirmation_link: str = (
            settings.FRONTEND_URL + '/confirm-email/' + confirmation_token.token
        )
        send_confirmation_mail.delay(**mail_data, confirmation_link=confirmation_link)

    def _get_user_by_token(self, token: str) -> Optional[User]:
        """
        _get_user_by_token: Return user object from token or None if token is not correct.

        Args:
            token (str): confirmation token.

        Returns:
            Optional[User]: User if token is correct otherwise None.
        """

        confirmation_token: Token = self.token_class(token=token, type='access')

        if not confirmation_token.verify():
            return None

        user: Optional[User] = confirmation_token.get_user_by_token()

        return user

    def set_user_as_verified(self, dto: ConfirmationTokenDTO) -> None:
        """
        set_user_as_verified: Make user verified if token is correct otherwise throw exception.

        Args:
            dto (ConfirmationTokenDTO): ConfirmationTokenDTO

        Raises:
            ParseError: Bad token.
        """

        token_data: dict[str, str] = self._prepare_token(dto)
        user: Optional[User] = self._get_user_by_token(**token_data)

        if user is None:
            raise ParseError(detail='Bad token.')

        user.set_is_verified(True)

    def send_reset_password_link(self, dto: EmailDTO) -> None:
        """
        send_reset_password_link: Send reset password link to email address.

        Args:
            dto (EmailDTO): EmailDTO.
        """

        mail_data: dict[str, str] = self._prepare_email(dto)
        user: User = get_object_or_404(self.model_class, **mail_data)
        confirmation_token, _ = self.token_class.for_user(user)
        confirmation_link: str = (
            settings.FRONTEND_URL + '/reset-password/' + confirmation_token.token
        )
        send_confirmation_mail.delay(**mail_data, confirmation_link=confirmation_link)

    def reset_user_password(self, token_dto: ConfirmationTokenDTO, passw_dto: PasswordDTO) -> None:
        """
        reset_user_password: Set new password User password after reseting.

        Args:
            token_dto (ConfirmationTokenDTO): ConfirmationTokenDTO.
            passw_dto (PasswordDTO): PasswordDTO.

        Raises:
            ParseError: Bad token.
        """

        token_data: dict[str, str] = self._prepare_token(token_dto)
        password_data: dict[str, str] = self._prepare_password(passw_dto)
        user: Optional[User] = self._get_user_by_token(**token_data)

        if user is None:
            raise ParseError(detail='Bad token.')

        user.set_password(**password_data)
