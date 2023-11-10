"""
apps.py: File, containing config for core application.
"""


from typing import ClassVar
from django.apps import AppConfig


class CoreConfig(AppConfig):
    """
    CoreConfig: Config class for a core application.

    Args:
        AppConfig (_type_): Builtin config superclass.
    """

    default_auto_field: ClassVar[str] = 'django.db.models.BigAutoField'
    name: ClassVar[str] = 'core'
    label: ClassVar[str] = 'core'
    verbose_name: ClassVar[str] = 'Core application'
