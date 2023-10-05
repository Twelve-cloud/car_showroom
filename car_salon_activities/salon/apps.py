"""
apps.py: Config file for a salon application.
"""


from typing import ClassVar

from django.apps import AppConfig


class SalonConfig(AppConfig):
    """
    SalonConfig: Config class for an salon application.

    Args:
        AppConfig (_type_): Builtin config superclass.
    """

    default_auto_field: ClassVar[str] = 'django.db.models.BigAutoField'
    name: ClassVar[str] = 'salon'
    label: ClassVar[str] = 'salon'
    verbose_name: ClassVar[str] = 'Car Salon Activities'
