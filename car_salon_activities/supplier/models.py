"""
models.py: File, containing models for supplier app.
"""


from typing import ClassVar
from django.db import models
from django.core import validators
from core.models import BaseModel


class SupplierModel(BaseModel):
    """
    SupplierModel: Represents supplier.

    Args:
        BaseModel (_type_): BaseModel (_type_): Base model for every model in the project.
    """

    name = models.CharField(
        verbose_name='name of the supplier',
    )

    year = models.PositiveIntegerField(
        validators=[validators.MinValueValidator(1900)],
        verbose_name='creation year',
    )

    customers_count = models.PositiveIntegerField(
        default=0,
        validators=[validators.MinValueValidator(0)],
        verbose_name='number of customers',
    )

    number_of_sales = models.PositiveIntegerField(
        default=20,
        validators=[validators.MinValueValidator(0)],
        verbose_name='number of sales after which discount is provided',
    )

    discount_for_unique_castomers = models.DecimalField(
        default=0.2,
        max_digits=3,
        decimal_places=2,
        validators=[
            validators.MinValueValidator(0.0),
            validators.MaxValueValidator(0.5),
        ],
        verbose_name='discount precent for unique customers',
    )

    class Meta:
        verbose_name: ClassVar[str] = 'Supplier'
        verbose_name_plural: ClassVar[str] = 'Suppliers'
        db_table: ClassVar[str] = 'Supplier'


class SupplierCarDiscount(BaseModel):
    """
    SupplierCarDiscount: Represents discount that is provided by supplier.

    Args:
        BaseModel (_type_): BaseModel (_type_): Base model for every model in the project.
    """

    name = models.CharField(
        verbose_name='discount name',
    )

    description = models.TextField(
        verbose_name='discount description',
    )

    precent = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[
            validators.MinValueValidator(0.0),
            validators.MaxValueValidator(0.5),
        ],
        verbose_name='discount precent',
    )

    start_date = models.DateTimeField(
        verbose_name='start date of the discount',
    )

    finish_date = models.DateTimeField(
        verbose_name='finish date of the discount',
    )

    supplier = models.ForeignKey(
        SupplierModel,
        on_delete=models.CASCADE,
        related_name='discounts',
        related_query_name='discounts',
        verbose_name='supplier which provides discount',
    )

    class Meta:
        verbose_name: ClassVar[str] = 'Supplier discount'
        verbose_name_plural: ClassVar[str] = 'Supplier discounts'
        db_table: ClassVar[str] = 'SupplierDiscount'


class SupplierCar(BaseModel):
    """
    SupplierCar: Represents car of the supplier.

    Args:
        BaseModel (_type_): Base model for every model in the project.
    """

    price = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        validators=[validators.MinValueValidator(0.0)],
        verbose_name='price of the car',
    )

    supplier = models.ForeignKey(
        SupplierModel,
        on_delete=models.CASCADE,
        related_name='cars',
        related_query_name='cars',
        verbose_name='supplier that owns cars',
    )

    discount = models.ForeignKey(
        SupplierCarDiscount,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='cars',
        related_query_name='cars',
        verbose_name='car discount',
    )

    class Meta:
        verbose_name: ClassVar[str] = 'Supplier car'
        verbose_name_plural: ClassVar[str] = 'Supplier cars'
        db_table: ClassVar[str] = 'SupplierCar'


class SupplierHistory(BaseModel):
    """
    SupplierHistory: Represents history entry of the supplier.

    Args:
        BaseModel (_type_): Base model for every model in the project.
    """

    supplier = models.ForeignKey(
        SupplierModel,
        on_delete=models.CASCADE,
        related_name='history',
        related_query_name='history',
        verbose_name='supplier which owns history entry',
    )

    car = models.CharField(
        verbose_name='car',
    )

    sale_price = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        validators=[validators.MinValueValidator(0.0)],
        verbose_name='sale price',
    )

    showroom = models.CharField(
        verbose_name='showroom',
    )

    class Meta:
        verbose_name: ClassVar[str] = 'Supplier history entry'
        verbose_name_plural: ClassVar[str] = 'Supplioer history'
        db_table: ClassVar[str] = 'SupplierHistory'
