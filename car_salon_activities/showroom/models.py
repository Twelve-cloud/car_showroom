"""
models.py: File, containing models for showroom app.
"""


from typing import ClassVar
from django.db import models
from django.core import validators
from django_countries.fields import CountryField
from core.models import CarModel, BaseModel
from customer.models import CustomerModel
from supplier.models import SupplierModel


class ShowroomModel(BaseModel):
    """
    ShowroomModel: Represents car showroom.

    Args:
        BaseModel (_type_): Base model for every model in the project.
    """

    name = models.CharField(
        max_length=50,
        verbose_name='name of the showroom',
    )

    creation_year = models.PositiveIntegerField(
        validators=[validators.MinValueValidator(1900)],
        verbose_name='creation year of the showroom',
    )

    balance = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0.0,
        validators=[validators.MinValueValidator(0.0)],
        verbose_name='balance',
    )

    location = CountryField()

    charts = models.JSONField(
        verbose_name='charts of appropriate cars',
    )

    appropriate_cars = models.ManyToManyField(
        CarModel,
        symmetrical=False,
        related_name='showrooms',
        related_query_name='showrooms',
        verbose_name='appropriate cars for the showroom',
    )

    current_suppliers = models.ManyToManyField(
        SupplierModel,
        symmetrical=False,
        related_name='showrooms',
        related_query_name='showrooms',
        verbose_name='current suppliers of the showroom',
    )

    number_of_sales = models.PositiveIntegerField(
        default=20,
        validators=[validators.MinValueValidator(0)],
        verbose_name='number of sales after which discount is provided',
    )

    discount_for_unique_customers = models.DecimalField(
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
        verbose_name: ClassVar[str] = 'Showroom'
        verbose_name_plural: ClassVar[str] = 'Showrooms'
        db_table: ClassVar[str] = 'Showroom'


class ShowroomCarDiscount(BaseModel):
    """
    ShowroomCarDiscount: Represents discount that is provided by showroom.

    Args:
        BaseModel (_type_): Base model for every model in the project.
    """

    name = models.CharField(
        max_length=50,
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

    showroom = models.ForeignKey(
        ShowroomModel,
        on_delete=models.CASCADE,
        related_name='discounts',
        related_query_name='discounts',
        verbose_name='showroom which provides discount',
    )

    class Meta:
        verbose_name: ClassVar[str] = 'Showroom discount'
        verbose_name_plural: ClassVar[str] = 'Showroom discounts.'
        db_table: ClassVar[str] = 'ShowroomDiscount'


class ShowroomCar(BaseModel):
    """
    ShowroomCar: Represents car of the showroom.

    Args:
        BaseModel (_type_): Base model for every model in the project.
    """

    price = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        validators=[validators.MinValueValidator(0.0)],
        verbose_name='price of the car',
    )

    showroom = models.ForeignKey(
        ShowroomModel,
        on_delete=models.CASCADE,
        related_name='cars',
        related_query_name='cars',
        verbose_name='showroom that owns cars',
    )

    discount = models.ForeignKey(
        ShowroomCarDiscount,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='cars',
        related_query_name='cars',
        verbose_name='car discount',
    )

    user = models.ForeignKey(
        CustomerModel,
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
        related_name='cars',
        related_query_name='cars',
        verbose_name='user who has bought the car',
    )

    class Meta:
        verbose_name: ClassVar[str] = 'Showroom car'
        verbose_name_plural: ClassVar[str] = 'Showroom cars'
        db_table: ClassVar[str] = 'ShowroomCar'


class ShowroomHistory(BaseModel):
    """
    ShowroomHistory: Represents history entry of the showroom.

    Args:
        BaseModel (_type_): Base model for every model in the project.
    """

    showroom = models.ForeignKey(
        ShowroomModel,
        on_delete=models.CASCADE,
        related_name='history',
        related_query_name='history',
        verbose_name='showroom which owns history entry',
    )

    car = models.CharField(
        max_length=50,
        verbose_name='car',
    )

    sale_price = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        validators=[validators.MinValueValidator(0.0)],
        verbose_name='sale price',
    )

    customer = models.CharField(
        max_length=50,
        verbose_name='customer',
    )

    class Meta:
        verbose_name: ClassVar[str] = 'Showroom history entry'
        verbose_name_plural: ClassVar[str] = 'Showroom history'
        db_table: ClassVar[str] = 'ShowroomHistory'
