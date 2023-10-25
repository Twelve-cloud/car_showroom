"""
sevices.py: File, containing services for a customer application.
"""


from customer.models import CustomerModel


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
