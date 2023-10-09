"""
apps.py: Config file for a jauth application.
"""


from typing import ClassVar
from django.apps import AppConfig


class JauthConfig(AppConfig):
    """
    JauthConfig: Config class for a jauth application.

    Args:
        AppConfig (_type_): Builtin config superclass.
    """

    default_auto_field: ClassVar[str] = 'django.db.models.BigAutoField'
    name: ClassVar[str] = 'jauth'
    label: ClassVar[str] = 'jauth'
    verbose_name: ClassVar[str] = 'JWT Authentification'
