"""
test_commands.py: File, containing tests for core.management.commands.
"""


import pytest
from core.models import CarModel
from supplier.models import SupplierCar, SupplierModel, SupplierCarDiscount
from core.management.commands.fill import Command


class TestFillCommand:
    @pytest.fixture(scope='function', autouse=True)
    def command(self):
        self.command = Command()

    def test_handle(self, mocker):
        cars = mocker.MagicMock()
        mocker.patch.object(Command, '_generate_cars', cars)

        suppliers = mocker.MagicMock()
        mocker.patch.object(Command, '_generate_suppliers', suppliers)

        supplier_cars = mocker.MagicMock()
        mocker.patch.object(Command, '_generate_supplier_cars', supplier_cars)

        supplier_discounts = mocker.MagicMock()
        mocker.patch.object(Command, '_generate_supplier_discounts', supplier_discounts)

        self.command.handle()

        cars.assert_called_once()
        suppliers.assert_called_once()
        supplier_cars.assert_called_once()
        supplier_discounts.assert_called_once()

    def test_generate_cars(self, mocker):
        mock = mocker.MagicMock()
        mocker.patch.object(CarModel.objects, 'get_or_create', mock)
        self.command._generate_cars()

        assert mock.call_count == 9

    def test_generate_suppliers(self, mocker):
        mock = mocker.MagicMock()
        mocker.patch.object(SupplierModel.objects, 'get_or_create', mock)
        self.command._generate_suppliers()

        assert mock.call_count == 14

    def test_generate_supplier_cars(self, mocker):
        mock = mocker.MagicMock()
        mocker.patch.object(SupplierCar.objects, 'get_or_create', mock)
        suppliers = mocker.MagicMock(return_value={'id__min': 1, 'id__max': 1})
        mocker.patch.object(SupplierModel.objects, 'aggregate', suppliers)
        cars = mocker.MagicMock(return_value={'id__min': 1, 'id__max': 1})
        mocker.patch.object(CarModel.objects, 'aggregate', cars)
        mocker.patch.object(SupplierModel.objects, 'get', mocker.MagicMock())
        mocker.patch.object(CarModel.objects, 'get', mocker.MagicMock())
        self.command._generate_supplier_cars()

        assert mock.call_count == 999

    def test_generate_supplier_discounts(self, mocker):
        mock = mocker.MagicMock(return_value=[SupplierCarDiscount(id=1), True])
        mocker.patch.object(SupplierCarDiscount.objects, 'get_or_create', mock)
        cars = mocker.MagicMock(return_value={'id__min': 1, 'id__max': 2})
        mocker.patch.object(CarModel.objects, 'aggregate', cars)
        mocker.patch.object(SupplierModel.objects, 'all', mocker.MagicMock(return_value=range(100)))
        discount = mocker.MagicMock()
        mocker.patch.object(SupplierCarDiscount, 'cars', discount)
        self.command._generate_supplier_discounts()

        assert discount.add.call_count == 100
        assert mock.call_count == 100

        mock = mocker.MagicMock(return_value=[SupplierCarDiscount(id=1), False])
        mocker.patch.object(SupplierCarDiscount.objects, 'get_or_create', mock)
        discount = mocker.MagicMock()
        mocker.patch.object(SupplierCarDiscount, 'cars', discount)
        self.command._generate_supplier_discounts()

        assert discount.add.call_count == 0
        assert mock.call_count == 100

    def test_generate_random_string(self):
        str1 = self.command._generate_random_string()
        str2 = self.command._generate_random_string()

        assert str1 != str2
        assert type(str1) is str and type(str2) is str
