"""
sevices.py: File, containing services for a showroom application.
"""


import json
from rest_framework.exceptions import ParseError
from core.models import CarModel
from showroom.models import ShowroomModel


class ShowroomService:
    """
    ShowroomService: Contains business logic for Showroom resourse.
    """

    def find_appropriate_cars(self, data: dict) -> filter[CarModel]:
        charts = data['charts']
        res = json.loads(charts)

        try:
            cars = [CarModel.objects.filter(**car_charts).first() for car_charts in res]
            return filter(lambda car: car is not None, cars)
        except Exception:
            raise ParseError('Invalid json data')

    def add_appropriate_cars(self, showroom: ShowroomModel, cars: filter[CarModel]) -> None:
        showroom.appropriate_cars.add(*cars)

    def delete_showroom(self, showroom: ShowroomModel) -> None:
        """
        delete_showroom: Sets showroom's is_active field to False.

        Args:
            showroom (ShowroomModel): Showroom instance.
        """

        showroom.is_active = False
        showroom.save()
