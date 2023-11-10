"""
test_services.py: File, containing tests for supplier.services.
"""


import pytest
from supplier.models import SupplierCar, SupplierModel, SupplierHistory, SupplierCarDiscount
from supplier.services import SupplierService


class TestSupplierService:
    @pytest.fixture(scope='function', autouse=True)
    def supplier_service(self):
        self.service = SupplierService()

    @pytest.fixture(scope='function', autouse=True)
    def supplier(self):
        self.supplier = SupplierModel(id=1, name='supplier')

    def test_delete_supplier(self, mocker):
        discount_mock = mocker.MagicMock()
        mocker.patch.object(SupplierCarDiscount, 'save', discount_mock)
        mock = mocker.MagicMock()
        supplier_discount = SupplierCarDiscount(id=1, is_active=True)
        mock.all.return_value = [supplier_discount]
        mocker.patch.object(SupplierModel, 'discounts', mock)

        car_mock = mocker.MagicMock()
        mocker.patch.object(SupplierCar, 'save', car_mock)
        mock = mocker.MagicMock()
        supplier_car = SupplierCar(id=1, is_active=True)
        mock.all.return_value = [supplier_car]
        mocker.patch.object(SupplierModel, 'cars', mock)

        history_mock = mocker.MagicMock()
        mocker.patch.object(SupplierHistory, 'save', history_mock)
        mock = mocker.MagicMock()
        supplier_history = SupplierHistory(id=1, is_active=True)
        mock.all.return_value = [supplier_history]
        mocker.patch.object(SupplierModel, 'history', mock)

        self.supplier.is_active = True
        self.service.delete_supplier(self.supplier)

        discount_mock.assert_called_once()
        assert supplier_discount.is_active is False

        car_mock.assert_called_once()
        assert supplier_car.is_active is False

        history_mock.assert_called_once()
        assert supplier_history.is_active is False

        assert self.supplier.is_active is False
