"""
apps.py: Config file for an auth application.
"""


from typing import ClassVar

from django.apps import AppConfig


class AuthConfig(AppConfig):
    """
    AuthConfig: Config class for an auth application.

    Args:
        AppConfig (_type_): Builtin config superclass.
    """

    default_auto_field: ClassVar[str] = 'django.db.models.BigAutoField'
    name: ClassVar[str] = 'auth'
    label: ClassVar[str] = 'auth'
    verbose_name: ClassVar[str] = 'JWT Authentification'
