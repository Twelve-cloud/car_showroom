"""
apps.py: File, containing config for showroom application.
"""


from typing import ClassVar
from django.apps import AppConfig


class ShowroomConfig(AppConfig):
    """
    ShowroomConfig: Config class for a showroom application.

    Args:
        AppConfig (_type_): Builtin config superclass.
    """

    default_auto_field: ClassVar[str] = 'django.db.models.BigAutoField'
    name: ClassVar[str] = 'showroom'
    label: ClassVar[str] = 'showroom'
    verbose_name: ClassVar[str] = 'Showroom application'
