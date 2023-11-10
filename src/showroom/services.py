"""
sevices.py: File, containing services for a showroom application.
"""


import json
from typing import Iterable
from rest_framework.exceptions import ParseError
from core.tasks import find_suppliers
from core.models import CarModel
from showroom.models import ShowroomModel


class ShowroomService:
    """
    ShowroomService: Contains business logic for Showroom resourse.
    """

    def find_appropriate_cars(self, data: dict) -> Iterable[CarModel]:
        """
        find_appropriate_cars: Finds appropriate cars for showroom.

        Args:
            data (dict): Data from request.

        Raises:
            ParseError: If json-field 'charts' is not correct.

        Returns:
            Iterable[CarModel]: Cars iterable object.
        """

        charts: str | list = data['charts']
        cars_charts: list = json.loads(charts) if type(charts) is str else charts

        try:
            cars: list = [
                CarModel.objects.filter(**car_charts).first() for car_charts in cars_charts
            ]
            return filter(lambda car: car is not None, cars)
        except Exception:
            raise ParseError('Invalid json data')

    def add_appropriate_cars(self, showroom: ShowroomModel, cars: Iterable[CarModel]) -> None:
        """
        add_appropriate_cars: Adds appropriate cars to appropriate_cars field of showroom.

        Args:
            showroom (ShowroomModel): Showroom instance.
            cars (Iterable[CarModel]): Car instance.
        """

        showroom.appropriate_cars.clear()
        showroom.appropriate_cars.add(*cars)

    def find_appropriate_suppliers(self, showroom: ShowroomModel) -> None:
        """
        find_appropriate_suppliers: Finds appropriate supplier for the showroom.

        Args:
            showroom (ShowroomModel): Showroom instance.
        """

        find_suppliers.delay(showroom.pk)

    def delete_showroom(self, showroom: ShowroomModel) -> None:
        """
        delete_showroom: Sets showroom's is_active field to False.

        Args:
            showroom (ShowroomModel): Showroom instance.
        """

        showroom.is_active = False
        showroom.save()

        for discount in showroom.discounts.all():
            discount.is_active = False
            discount.save()

        for car in showroom.cars.all():
            car.is_active = False
            car.save()

        for history_entry in showroom.history.all():
            history_entry.is_active = False
            history_entry.save()
