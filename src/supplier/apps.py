"""
apps.py: File, containing config for supplier application.
"""


from typing import ClassVar
from django.apps import AppConfig


class SupplierConfig(AppConfig):
    default_auto_field: ClassVar[str] = 'django.db.models.BigAutoField'
    name: ClassVar[str] = 'supplier'
    label: ClassVar[str] = 'supplier'
    verbose_name: ClassVar[str] = 'Supplier application'
