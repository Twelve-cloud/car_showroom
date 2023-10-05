"""
"""


from django.contrib.auth.hashers import check_password, make_password
from django.core import validators
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save)
def pre_save_handler(sender, instance, update_fields, **kwargs):
    instance.full_clean()

    if instance._state.adding:
        instance.set_password(instance.password)


class User(models.Model):
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
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'User'

    def get_username(self):
        return self.username

    def __str__(self):
        return self.get_username()

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        def setter(raw_password):
            self.set_password(raw_password)
            self.save(update_fields=['password'])

        return check_password(raw_password, self.password, setter)

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()

    def get_short_name(self):
        return self.first_name.strip()
