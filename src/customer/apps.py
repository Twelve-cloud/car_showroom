"""
apps.py: File, containing config for customer application.
"""


from typing import ClassVar
from django.apps import AppConfig


class CustomerConfig(AppConfig):
    """
    CustomerConfig: Config class for a customer application.

    Args:
        AppConfig (_type_): Builtin config superclass.
    """

    default_auto_field: ClassVar[str] = 'django.db.models.BigAutoField'
    name: ClassVar[str] = 'customer'
    label: ClassVar[str] = 'customer'
    verbose_name: ClassVar[str] = 'Customer application'
