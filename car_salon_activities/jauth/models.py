"""
models.py: File, containing models for a jauth application.
"""


from typing import ClassVar
from django.db import models
from django.core import validators
from django.dispatch import receiver
from django.db.models.signals import pre_save
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

    class Meta:
        verbose_name: ClassVar[str] = 'User'
        verbose_name_plural: ClassVar[str] = 'Users'
        db_table: ClassVar[str] = 'User'

    def get_username(self) -> str:
        return self.username

    def __str__(self) -> str:
        return self.get_username()

    def is_anonymous(self) -> bool:
        return False

    def is_authenticated(self) -> bool:
        return True

    def set_password(self, raw_password: str) -> None:
        self.password = make_password(raw_password)

    def check_password(self, raw_password: str) -> bool:
        def setter(raw_password: str) -> None:
            self.set_password(raw_password)
            self.save(update_fields=['password'])

        return check_password(raw_password, self.password, setter)

    def get_full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'.strip()

    def get_short_name(self) -> str:
        return self.first_name.strip()


@receiver(pre_save, sender=User)
def pre_save_handler(sender: type[User], instance: User, **kwargs: dict) -> None:
    """
    pre_save_handler: Function, performing before .save() is called.
    It starts full validation of the record and encrypt password.

    Args:
        sender (type[User]): User model.
        instance (User): Instance of the User model.
    """

    instance.full_clean()

    if instance._state.adding:
        instance.set_password(instance.password)
    else:
        old_instance = sender.objects.get(pk=instance.pk)
        if old_instance.password != instance.password:
            instance.set_password(instance.password)
