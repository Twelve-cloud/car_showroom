"""
fill.py: File, containing commands for a project.
"""


from random import choice, choices, randint, uniform
from string import digits, ascii_uppercase
from datetime import datetime, timedelta
from django.db.models import Max, Min
from django.core.management.base import BaseCommand
from core.models import CarModel
from supplier.models import SupplierCar, SupplierModel, SupplierCarDiscount


class Command(BaseCommand):
    """
    Command: Generates suppliers data for database.

    Args:
        BaseCommand (_type_): Builtin superclass for a FillDbCommand.
    """

    def handle(self, *args: tuple, **options: dict) -> None:
        """
        handle: Main entrypoint that will be called when it is applied as manage.py command.
        """

        self._generate_cars()
        self._generate_suppliers()
        self._generate_supplier_cars()
        self._generate_supplier_discounts()

    def _generate_cars(self) -> None:
        """
        _generate_cars: Generates cars for a project.
        """

        for i in range(1, 10):
            CarModel.objects.get_or_create(
                brand=choice(CarModel.Brands.choices)[0],
                transmission_type=choice(CarModel.TransmissionTypes.choices)[0],
                creation_year=randint(1900, datetime.now().year),
                miliage=randint(1000, 200000),
            )

    def _generate_suppliers(self) -> None:
        """
        _generate_suppliers: Generates suppliers for a project.
        """

        for i in range(1, 15):
            SupplierModel.objects.get_or_create(
                name=f'supplier#{self._generate_random_string()}',
                creation_year=randint(1900, datetime.now().year),
                customers_count=0,
                number_of_sales=randint(10, 30),
                discount_for_unique_customers=uniform(0.2, 0.5),
            )

    def _generate_supplier_cars(self) -> None:
        """
        _generate_supplier_cars: Generates supplier cars for a project.
        """

        supplier_ids: dict = SupplierModel.objects.aggregate(Min('id'), Max('id'))
        car_ids: dict = CarModel.objects.aggregate(Min('id'), Max('id'))

        for i in range(1, 1000):
            SupplierCar.objects.get_or_create(
                supplier=SupplierModel.objects.get(
                    id=randint(supplier_ids['id__min'], supplier_ids['id__max'])
                ),
                car=CarModel.objects.get(
                    id=randint(car_ids['id__min'], car_ids['id__max']),
                ),
                price=randint(1000, 100000),
            )

    def _generate_supplier_discounts(self) -> None:
        """
        _generate_supplier_discounts: Generates discounts for every supplier for a project.
        """

        car_ids: dict = CarModel.objects.aggregate(Min('id'), Max('id'))
        car_ids_list: range = range(car_ids['id__min'], car_ids['id__max'])

        for supplier in SupplierModel.objects.all():
            discount, created = SupplierCarDiscount.objects.get_or_create(
                name=f'discount#{self._generate_random_string()}',
                description=f'description#{self._generate_random_string()}',
                precent=uniform(0, 0.5),
                start_date=datetime.now(),
                finish_date=datetime.now() + timedelta(hours=randint(1, 5)),
                supplier=supplier,
            )

            if created is True:
                discount.cars.add(*choices(car_ids_list, k=2))

    def _generate_random_string(self) -> str:
        """
        _generate_random_string: Generates random string.

        Returns:
            str: Random string.
        """

        return ''.join(choices(ascii_uppercase + digits, k=5))
