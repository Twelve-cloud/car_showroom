"""
sevices.py: File, containing services for a customer application.
"""


from customer.models import CustomerModel


class CustomerService:
    def delete_customer(self, customer: CustomerModel) -> None:
        customer.is_active = False
        customer.save()
