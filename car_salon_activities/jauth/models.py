"""
models.py: File, containing models for an jauth application.
"""


from typing import ClassVar
from datetime import datetime
from django.db import models
from django.core import validators
from django.contrib.auth.hashers import make_password, check_password


class User(models.Model):
    """
    User: Custom User model.

    Args:
        models.Model (_type_): Builtin superclass for a custom User model.
    """

    username = models.CharField(
        max_length=32,
        unique=True,
        verbose_name='username',
        db_index=True,
        validators=[validators.MinLengthValidator(8)],
    )

    email = models.EmailField(
        max_length=320,
        unique=True,
        verbose_name='email',
        db_index=True,
        validators=[validators.MinLengthValidator(3)],
    )

    password = models.CharField(
        max_length=128,
        verbose_name='password',
        validators=[validators.MinLengthValidator(8)],
    )

    first_name = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        verbose_name='first name',
    )

    last_name = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        verbose_name='last name',
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name='date joined',
    )

    last_updated = models.DateTimeField(
        auto_now=True,
        verbose_name='last updated',
    )

    last_login = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='last login',
    )

    is_active = models.BooleanField(
        default=False,
        verbose_name='is active',
    )

    is_staff = models.BooleanField(
        default=False,
        verbose_name='is staff',
    )

    is_verified = models.BooleanField(
        default=False,
        verbose_name='is verified',
    )

    def set_password(self, password: str) -> None:
        """
        set_password: Set password to the current user.

        Args:
            password (str): New password.
        """

        self.password = make_password(password)
        self.save(update_fields=['password'])

    def check_password(self, password: str) -> bool:
        """
        check_password: Check if password is correct.

        Args:
            rpassword (str): Specified password.

        Returns:
            bool: True if password is correct otherwise False.
        """

        return check_password(password, self.password, self.set_password)

    def set_first_name(self, first_name: str) -> None:
        """
        set_first_name: Set first name to the current user.

        Args:
            first_name (str): New first name.
        """

        self.first_name = first_name
        self.save(update_fields=['first_name'])

    def set_last_name(self, last_name: str) -> None:
        """
        set_last_name: Set last name to the current user.

        Args:
            last_name (str): New last name.
        """

        self.last_name = last_name
        self.save(update_fields=['last_name'])

    def set_last_login(self, last_login: datetime = datetime.now()) -> None:
        """
        set_last_login: Set last login date to the current user.

        Args:
            last_login (datetime): New last login date.
        """

        self.last_login = last_login
        self.save(update_fields=['last_login'])

    def set_is_active(self, is_active: bool) -> None:
        """
        set_is_active: Set user active status.

        Args:
            is_active (bool): New active status.
        """

        self.is_active = is_active
        self.save(update_fields=['is_active'])

    def set_is_staff(self, is_staff: bool) -> None:
        """
        set_is_staff: Set user staff status.

        Args:
            is_staff (bool): New staff status.
        """

        self.is_staff = is_staff
        self.save(update_fields=['is_staff'])

    def set_is_verified(self, is_verified: bool) -> None:
        """
        set_is_verified: Set user verified status.

        Args:
            is_verified (bool): New verified status.
        """

        self.is_verified = is_verified
        self.save(update_fields=['is_verified'])

    def is_anonymous(self) -> bool:
        """
        is_anonymous: Checks if User is Anonymous.

        Returns:
            bool: Everytime False,  because if user is anon then request user is None.
        """

        return False

    def is_authenticated(self) -> bool:
        """
        is_authenticated: Checks if User if authenticated.

        Returns:
            bool: Everytime True, because if user is not authenticated then request user is None.
        """

        return True

    def __str__(self) -> str:
        """
        __str__: Return user instance representation.

        Returns:
            str: User instance representation.
        """

        return self.username

    class Meta:
        """
        Meta: Class, providing medata for custom User model.
        """

        verbose_name: ClassVar[str] = 'User'
        verbose_name_plural: ClassVar[str] = 'Users'
        ordering: ClassVar[list] = ['pk']
        db_table: ClassVar[str] = 'User'
