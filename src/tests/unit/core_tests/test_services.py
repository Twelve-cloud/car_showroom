"""
test_services.py: File, containing unit tests for core.services.
"""


import pytest
from core.models import CarModel
from core.services import CarService


class TestCarService:
    @pytest.fixture(scope='function', autouse=True)
    def car_service(self):
        self.service = CarService()

    @pytest.fixture(scope='function', autouse=True)
    def car(self):
        self.car = CarModel()

    def test_set_car_as_inactive(self):
        self.car.is_active = True
        self.service.set_car_as_inactive(self.car)

        assert self.car.is_active is False
