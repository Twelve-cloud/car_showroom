"""
sevices.py: File, containing services for a jauth application.
"""


from typing import ClassVar, Optional
from django.conf import FRONTEND_URL
from jauth.tasks import send_confirmation_mail
from jauth.models import User
from jauth.tokens import Token


class UserService:
    """
    UserService: Contains business logic of user.
    """

    token_class: ClassVar[type[Token]] = Token
    model_class: ClassVar[type[User]] = User

    def send_confirmation_link(self, email: str) -> None:
        """
        send_confirmation_link: Creates confrimation link and sends it to user's email address.

        Args:
            email (str): Email address of the user.
        """

        user: User = self.model_class.objects.get(email=email)
        confirmation_token, _ = self.token_class.for_user(user)
        confirmation_link: str = FRONTEND_URL + '/confirm-email/' + confirmation_token.token
        send_confirmation_mail.delay(email, confirmation_link)

    def send_reset_password_link(self, email: str) -> None:
        """
        send_reset_password_link: Creates confrimation link and sends it to user's email address.

        Args:
            email (str): Email address of the user.
        """

        user: User = self.model_class.objects.get(email=email)
        confirmation_token, _ = self.token_class.for_user(user)
        confirmation_link: str = FRONTEND_URL + '/reset-password/' + confirmation_token.token
        send_confirmation_mail.delay(email, confirmation_link)

    def get_user_by_token(self, confirmation_token: str) -> Optional[User]:
        """
        get_user_by_token: Returns user according to token or None if token is not valid.

        Args:
            confirmation_token (str): User's confirmation token.

        Returns:
            Optional[User]: User instance or None if token is not valid.
        """

        token: Token = self.token_class(token=confirmation_token, type='access')

        if not token.verify():
            return None

        user: User = token.get_user_by_token()
        return user

    def set_user_as_inactive(self, user: User) -> None:
        """
        set_user_as_inactive: Sets user's is_active field to False.

        Args:
            user (User): User instance.
        """

        user.is_active = False
        user.save()

    def set_user_as_not_verified(self, user: User) -> None:
        """
        set_user_as_not_verified: Sets user's is_verified field to False.

        Args:
            user (User): User instance.
        """

        user.is_verified = False
        user.save()

    def set_user_as_verified(self, user: User) -> None:
        """
        set_user_as_verified: Sets user's is_verified field to True.

        Args:
            user (User): User instance.
        """

        user.is_verified = True
        user.save()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        get_user_by_email: Returns user by email or none if user with specified email doesn't exist.

        Args:
            email (str): Email of the user.

        Returns:
            Optional[User]: User instance or None.
        """

        user = User.objects.filter(email=email).first()
        return user
