"""
tasks.py: File, containing celery tasks for a core application.
"""


from datetime import datetime
from celery import shared_task
from showroom.models import ShowroomCarDiscount
from supplier.models import SupplierCarDiscount


@shared_task
def delete_finished_discounts() -> None:
    """
    delete_finished_discounts: Deletes discounts that are finished.
    """

    finished_discounts: list = [
        ShowroomCarDiscount,
        SupplierCarDiscount,
    ]

    for discount_class in finished_discounts:
        discount_class.objects.filter(finish_date__lt=datetime.now()).update(is_active=False)
