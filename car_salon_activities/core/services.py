"""
sevices.py: File, containing services for a core application.
"""


from core.models import CarModel


class CarService:
    """
    CarService: Contains business logic of car.
    """

    def set_car_as_inactive(self, car: CarModel) -> None:
        car.is_active = False
        car.save()
