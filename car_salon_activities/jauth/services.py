"""
sevices.py: File, containing services for a jauth application.
"""


from typing import Optional
from jauth.tasks import send_verification_mail
from jauth.models import User
from jauth.tokens import Token


class UserService:
    """
    UserService: Contains low-level User services.
    """

    token_class = Token
    model_class = User
    base_link = ''

    def send_verification_link(self, email: str) -> None:
        """
        send_verification_link: Creates verification link and sends it to user's email address.

        Args:
            email (str): Email address of the user.
        """

        user = self.model_class.objects.get(email=email)
        verification_token, _ = self.token_class.for_user(user)
        verification_link = self.base_link + verification_token.token
        send_verification_mail.delay(email, verification_link)

    def get_user_by_token(self, verification_token: str) -> Optional[User]:
        """
        get_user_by_token: Returns user according to token or None if token is not valid.

        Args:
            verification_token (str): User's verification token.

        Returns:
            Optional[User]: User instance or None if token is not valid.
        """

        token = self.token_class(token=verification_token, type='access')

        if not token.verify():
            return None

        user = token.get_user_by_token()
        return user

    def set_user_as_active(self, user: User) -> None:
        """
        set_user_as_active: Sets user's is_active and is_verified fields to True.

        Args:
            user (User): User instance.
        """

        user.is_active = True
        user.is_verified = True
        user.save()

    def set_user_as_inactive(self, user: User) -> None:
        """
        set_user_as_inactive: Sets user's is_active field to False.

        Args:
            user (User): User instance.
        """

        user.is_active = False
        user.save()
