"""
test_services.py: File, containing tests for customer.services.
"""


import pytest
from core.tasks import make_customer_offer
from customer.models import CustomerModel
from customer.services import CustomerService


class TestCustomerService:
    @pytest.fixture(scope='function', autouse=True)
    def customer_service(self):
        self.service = CustomerService()

    @pytest.fixture(scope='function', autouse=True)
    def customer(self, user):
        self.customer = CustomerModel(balance=0.0, user=user)

    def test_delete_customer(self):
        self.customer.is_active = True
        self.service.delete_customer(self.customer)

        assert self.customer.is_active is False

    def test_make_offer(self, mocker):
        mock = mocker.MagicMock(return_value=True)
        mocker.patch.object(make_customer_offer, 'delay', mock)
        self.service.make_offer(mocker.MagicMock(spec=['id']))

        mock.assert_called_once()
