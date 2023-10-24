"""
models.py: File, containing basic models for whole project.
"""


from typing import ClassVar
from django.db import models
from django.core import validators


class BaseModel(models.Model):
    """
    BaseModel: Base model, which is inherited by any other model.

    Args:
        models.Model (_type_): Builtin superclass for base model.
    """

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='created at',
    )

    last_updated = models.DateTimeField(
        auto_now=True,
        verbose_name='last updated',
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='is active',
    )

    class Meta:
        abstract: ClassVar[bool] = True


class CarModel(BaseModel):
    """
    CarModel: Represents car and its characteristics.

    Args:
        BaseModel (_type_): Base model for every model in the project.
    """

    class Brands(models.TextChoices):
        """
        Brands: Brand choices.

        Args:
            models.TextChoices (_type_): Buildin superclass for Brands model.
        """

        AUDI: tuple[str, str] = 'audi', 'Audi'
        BMW: tuple[str, str] = 'bmw', 'BMW'
        TESLA: tuple[str, str] = 'tesla', 'Tesla'
        __empty__: str = 'Choose brand of the car.'

    class TransmissionTypes(models.TextChoices):
        """
        TransmissionTypes: Transmission types choices.

        Args:
            models.TextChoices (_type_): Buildin superclass for TransmissionTypes model.
        """

        MANUAL: tuple[str, str] = 'manual', 'Manual'
        AUTO: tuple[str, str] = 'auto', 'Automatic'
        __empty__: str = 'Choose transmission type of the car.'

    brand = models.CharField(
        choices=Brands.choices,
        verbose_name='brand of the car',
    )

    transmission_type = models.CharField(
        choices=TransmissionTypes.choices,
        verbose_name='transmission type of the car',
    )

    creation_year = models.PositiveIntegerField(
        validators=[validators.MinValueValidator(1900)],
        verbose_name='creation year of the car',
    )

    miliage = models.FloatField(
        validators=[validators.MinValueValidator(0.0)],
        verbose_name='miliage of the car',
    )

    class Meta:
        verbose_name: ClassVar[str] = 'Car'
        verbose_name_plural: ClassVar[str] = 'Cars'
        db_table: ClassVar[str] = 'Car'
