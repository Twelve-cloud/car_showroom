"""
tasks.py: File, containing celery tasks for a core application.
"""


from typing import Optional
from datetime import datetime
from celery import group, shared_task
from django.db.models import Max, Count
from django.db.models.query import QuerySet
from core.models import CarModel
from showroom.models import ShowroomCar, ShowroomModel, ShowroomHistory, ShowroomCarDiscount
from supplier.models import SupplierCar, SupplierModel, SupplierHistory, SupplierCarDiscount


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

    showrooms: ShowroomModel = ShowroomModel.objects.filter(is_active=True)
    group(find_suppliers.s(showroom.id) for showroom in showrooms)()


def normalize(showroom: ShowroomModel) -> list[tuple[CarModel, SupplierHistory]]:
    return [
        (car, supplier)
        for car, supplier in zip(showroom.appropriate_cars.all(), showroom.current_suppliers.all())
    ]


def get_cars_with_suppliers_by_priority(showroom: ShowroomModel, cars_to_suppliers: list) -> list:
    priority_to_car: dict = {}

    for history_entry in ShowroomHistory.objects.filter(showroom=showroom).annotate(Count('car')):
        priority_to_car[history_entry.car__count] = history_entry.car

    cars_by_priority: list = [priority_to_car[priority] for priority in sorted(priority_to_car)]

    for car in showroom.appropriate_cars.all():
        if car not in cars_by_priority:
            cars_by_priority.append(car)

    for car_by_priority in cars_by_priority:
        if car_by_priority not in showroom.appropriate_cars.all():
            cars_by_priority.remove(car_by_priority)

    cars_with_suppliers_by_priority: list = [
        (car, supplier)
        for car_by_priority in cars_by_priority
        for car, supplier in cars_to_suppliers
        if car_by_priority == car
    ]

    return cars_with_suppliers_by_priority


def get_unique_showroom_discount(showroom: ShowroomModel, supplier: SupplierModel) -> float:
    if supplier.number_of_sales <= len(showroom.supplier_history.all()):
        return supplier.discount_for_unique_customers
    return 1


def get_car_details_with_max_discount(car: CarModel) -> tuple[CarModel, float]:
    discount = min(
        SupplierCarDiscount.objects.filter(cars__pk=car.pk, is_active=True),
        key=lambda discount: discount.precent,
    )

    supplier, max_precent = discount.supplier, discount.precent
    supplier_car = SupplierCar.objects.filter(supplier=supplier, car=car).first()

    return supplier_car, max_precent


@shared_task
def buy_supplier_cars() -> None:
    for showroom in ShowroomModel.objects.all():
        cars_to_suppliers: list = normalize(showroom)

        cars_with_suppliers_by_priority: list = get_cars_with_suppliers_by_priority(
            showroom, cars_to_suppliers
        )

        for car, supplier in cars_with_suppliers_by_priority[:1]:
            supplier_car: SupplierCar = supplier.cars.filter(car=car).first()
            unique_showoom_discount: float = get_unique_showroom_discount(showroom, supplier)
            car_with_max_discount, discount = get_car_details_with_max_discount(car)

            if (
                supplier_car.price * unique_showoom_discount
                < car_with_max_discount.price * discount
            ):
                price = supplier_car.price * unique_showoom_discount
                chosen_car = supplier_car
                chosen_supplier = supplier
            else:
                price = car_with_max_discount.price * discount
                chosen_car = car_with_max_discount
                chosen_supplier = car_with_max_discount.supplier

            if showroom.balance > price:
                showroom_car = ShowroomCar.objects.create(
                    car=chosen_car.car, price=price, showroom=showroom, user=None
                )
                showroom.cars.add(showroom_car)
                showroom.balance -= price

                history: SupplierHistory = SupplierHistory.objects.create(
                    supplier=chosen_supplier, car=car, sale_price=price, showroom=showroom
                )
                showroom.supplier_history.add(history)
