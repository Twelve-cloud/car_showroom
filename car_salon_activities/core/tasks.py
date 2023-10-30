"""
tasks.py: File, containing celery tasks for a core application.
"""


from typing import Optional
from datetime import datetime
from celery import group, shared_task
from django.db.models import Max
from django.db.models.query import QuerySet
from core.models import CarModel
from showroom.models import ShowroomModel, ShowroomCarDiscount
from supplier.models import SupplierCar, SupplierModel, SupplierCarDiscount


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


def find_cheapest_car(car: CarModel) -> Optional[SupplierCar]:
    """
    find_cheapest_car: Finds the cheapest supplier car according some metrics.

    Args:
        car (CarModel): CarModel instance.

    Returns:
        Optional[SupplierCar]: SupplierCar instance.
    """

    supplier_cars: QuerySet = SupplierCar.objects.select_related(
        'supplier',
    ).filter(
        car=car,
        is_active=True,
    )

    purchase_metrics_count: int = (
        SupplierModel.objects.filter(
            is_active=True,
        )
        .aggregate(
            Max('number_of_sales'),
        )
        .get('number_of_sales__max')
    )

    cheapest_car: Optional[SupplierCar] = None

    min_total_price: float = float('inf')

    for supplier_car in supplier_cars:
        purchases_with_discount: int = (
            purchase_metrics_count - supplier_car.supplier.number_of_sales
        )

        total_price_for_hundred_purchases: float = (
            purchases_with_discount
            * supplier_car.price
            * supplier_car.supplier.discount_for_unique_customers
            + supplier_car.supplier.number_of_sales * supplier_car.price
        )

        if total_price_for_hundred_purchases < min_total_price:
            min_total_price = total_price_for_hundred_purchases
            cheapest_car = supplier_car

    return cheapest_car


@shared_task
def find_suppliers(showroom_id: int) -> None:
    """
    find_suppliers: Find supplier for every appropriate car of showroom.

    Args:
        showroom (ShowroomModel): Showroom instance.
    """

    showroom = ShowroomModel.objects.prefetch_related('appropriate_cars').get(pk=showroom_id)

    showroom.current_suppliers.clear()

    showroom.current_suppliers.add(
        *[
            car.supplier
            for car in map(find_cheapest_car, showroom.appropriate_cars.all())
            if car is not None
        ]
    )


@shared_task
def check_suppliers() -> None:
    """
    check_suppliers: Check if it is OK to continue working with suppliers.
    """

    showrooms: ShowroomModel = ShowroomModel.objects.all()
    group(find_suppliers.s(showroom.id) for showroom in showrooms)()
