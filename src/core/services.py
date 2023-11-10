"""
sevices.py: File, containing services for a core application.
"""


from core.models import CarModel


class CarService:
    """
    CarService: Contains business logic for Car resourse.
    """

    def set_car_as_inactive(self, car: CarModel) -> None:
        """
        set_car_as_inactive: Sets car's field is_active to False.

        Args:
            car (CarModel): Car instance.
        """

        car.is_active = False
        car.save()
