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
