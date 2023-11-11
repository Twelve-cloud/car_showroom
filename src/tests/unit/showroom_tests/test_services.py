"""
test_services.py: File, containing unit tests for showroom.services.
"""


import pytest
from core.tasks import find_suppliers
from core.models import CarModel
from showroom.models import ShowroomCar, ShowroomModel, ShowroomHistory, ShowroomCarDiscount
from showroom.services import ShowroomService


class TestShowroomService:
    @pytest.fixture(scope='function', autouse=True)
    def showroom_service(self):
        self.service = ShowroomService()

    @pytest.fixture(scope='function', autouse=True)
    def showroom(self):
        self.showroom = ShowroomModel(id=1, name='showroom')

    @pytest.fixture(scope='function', autouse=True)
    def charts(self):
        self.charts = {
            "charts": [
                {
                    "brand": "audi",
                    "transmission_type": "auto",
                    "creation_year": 2000,
                    "milliage": 20000.0,
                }
            ]
        }

    def test_find_appropriate_scars(self, mocker):
        mock = mocker.MagicMock()
        mocker.patch.object(CarModel, 'objects', mock)

        car = CarModel(id=1)
        mock.filter.return_value.first.return_value = car

        assert next(self.service.find_appropriate_cars(self.charts)) == car

        with pytest.raises(Exception):
            mock.filter.return_value.first.side_effect = Exception
            self.service.find_appropriate_cars({"charts": [{"wrong": "value"}]})

    def test_add_appropriate_cars(self, mocker):
        mock = mocker.MagicMock()
        mocker.patch.object(ShowroomModel, 'appropriate_cars', mock)
        self.service.add_appropriate_cars(self.showroom, [CarModel(id=1)])

        mock.clear.assert_called_once()
        mock.add.assert_called_once()

    def test_find_appropriate_supplier(self, mocker):
        mock = mocker.MagicMock()
        mocker.patch.object(find_suppliers, 'delay', mock)
        self.service.find_appropriate_suppliers(self.showroom)

        mock.assert_called_once()

    def test_delete_showroom(self, mocker):
        discount_mock = mocker.MagicMock()
        mocker.patch.object(ShowroomCarDiscount, 'save', discount_mock)
        mock = mocker.MagicMock()
        car_discount = ShowroomCarDiscount(id=1, is_active=True)
        mock.all.return_value = [car_discount]
        mocker.patch.object(ShowroomModel, 'discounts', mock)

        car_mock = mocker.MagicMock()
        mocker.patch.object(ShowroomCar, 'save', car_mock)
        mock = mocker.MagicMock()
        showroom_car = ShowroomCar(id=1, is_active=True)
        mock.all.return_value = [showroom_car]
        mocker.patch.object(ShowroomModel, 'cars', mock)

        history_mock = mocker.MagicMock()
        mocker.patch.object(ShowroomHistory, 'save', history_mock)
        mock = mocker.MagicMock()
        showroom_history = ShowroomHistory(id=1, is_active=True)
        mock.all.return_value = [showroom_history]
        mocker.patch.object(ShowroomModel, 'history', mock)

        self.showroom.is_active = True
        self.service.delete_showroom(self.showroom)

        discount_mock.assert_called_once()
        assert car_discount.is_active is False

        car_mock.assert_called_once()
        assert showroom_car.is_active is False

        history_mock.assert_called_once()
        assert showroom_history.is_active is False

        assert self.showroom.is_active is False
