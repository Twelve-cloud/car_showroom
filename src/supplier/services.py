"""
sevices.py: File, containing services for a supplier application.
"""


from supplier.models import SupplierModel


class SupplierService:
    """
    SupplierService: Contains business logic for Supplier resourse.
    """

    def delete_supplier(self, supplier: SupplierModel) -> None:
        """
        delete_supplier: Sets supplier's is_active field to False.

        Args:
            supplier (SupplierModel): Supplier instance.
        """

        supplier.is_active = False
        supplier.save()

        for discount in supplier.discounts.all():
            discount.is_active = False
            discount.save()

        for car in supplier.cars.all():
            car.is_active = False
            car.save()

        for history_entry in supplier.history.all():
            history_entry.is_active = False
            history_entry.save()
