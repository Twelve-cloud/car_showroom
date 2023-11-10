"""
sevices.py: File, containing services for a customer application.
"""


from core.tasks import make_customer_offer
from customer.models import CustomerModel, CustomerOffer


class CustomerService:
    """
    CustomerService: Contains business logic for Customer resourse.
    """

    def delete_customer(self, customer: CustomerModel) -> None:
        """
        delete_customer: Sets customer's field is_active to False.

        Args:
            customer (CustomerModel): Customer instance.
        """

        customer.is_active = False
        customer.save()

    def make_offer(self, offer: CustomerOffer) -> None:
        """
        make_offer: Makes customer's offer.

        Args:
            offer (CustomerOffer): CustomerOffer instance.
        """

        make_customer_offer.delay(offer.id)
