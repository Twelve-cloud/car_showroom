"""
models.py: File, containing models for customer app.
"""


from typing import ClassVar
from django.db import models
from django.core import validators
from core.models import CarModel, BaseModel
from jauth.models import User


class CustomerModel(BaseModel):
    """
    CustomerModel: Represents customer.

    Args:
        BaseModel (_type_): Base model for every model in the project.
    """

    balance = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0.0,
        validators=[validators.MinValueValidator(0.0)],
        verbose_name='balance',
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='user instance',
    )

    class Meta:
        verbose_name: ClassVar[str] = 'Customer'
        verbose_name_plural: ClassVar[str] = 'Customers'
        db_table: ClassVar[str] = 'Customer'


class CustomerOffer(BaseModel):
    """
    CustomerModel: Represents customer's offer.

    Args:
        BaseModel (_type_): Base model for every model in the project.
    """

    customer = models.ForeignKey(
        CustomerModel,
        on_delete=models.CASCADE,
        related_name='offers',
        related_query_name='offers',
        verbose_name='offer of the customer',
    )

    max_price = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        validators=[validators.MinValueValidator(0.0)],
        verbose_name='purchase price',
    )

    car = models.ForeignKey(
        CarModel,
        on_delete=models.CASCADE,
        related_name='customer_offers',
        related_query_name='customer offers',
        verbose_name='car specified in offer',
    )

    class Meta:
        verbose_name: ClassVar[str] = 'Customer offer'
        verbose_name_plural: ClassVar[str] = 'Customers offer'
        db_table: ClassVar[str] = 'CustomerOffer'


class CustomerHistory(BaseModel):
    """
    CustomerHistory: Represents history entry of the customer.

    Args:
        BaseModel (_type_): Base model for every model in the project.
    """

    customer = models.ForeignKey(
        CustomerModel,
        on_delete=models.CASCADE,
        related_name='history',
        related_query_name='history',
        verbose_name='customer which owns history entry',
    )

    car = models.ForeignKey(
        CarModel,
        on_delete=models.CASCADE,
        related_name='customer_cars',
        related_query_name='customer_cars',
        verbose_name='customer car',
    )

    purchase_price = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        validators=[validators.MinValueValidator(0.0)],
        verbose_name='purchase price',
    )

    showroom = models.CharField(
        max_length=50,
        verbose_name='showroom',
    )

    class Meta:
        verbose_name: ClassVar[str] = 'Customer history entry'
        verbose_name_plural: ClassVar[str] = 'Customer history'
        db_table: ClassVar[str] = 'CustomerHistory'
