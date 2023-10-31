"""
tasks.py: File, containing celery tasks for a core application.
"""


from typing import Optional
from datetime import datetime
from celery import group, shared_task
from django.db.models import Max, Count
from django.db.models.query import QuerySet
from core.models import CarModel
from customer.models import CustomerModel, CustomerOffer, CustomerHistory
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
    """
    normalize: Returns cars with suppliers that are solding these cats.

    Args:
        showroom (ShowroomModel): Showroom instance.

    Returns:
        list[tuple[CarModel, SupplierHistory]]: List where elements are (car, supplier).
    """

    return [
        (car, supplier)
        for car, supplier in zip(showroom.appropriate_cars.all(), showroom.current_suppliers.all())
    ]


def get_cars_with_suppliers_by_priority(showroom: ShowroomModel, cars_to_suppliers: list) -> list:
    """
    get_cars_with_suppliers_by_priority: Returns cars with supplier by priority.

    Args:
        showroom (ShowroomModel): Showroom instance.
        cars_to_suppliers (list): List with cars and suppliers.

    Returns:
        list: Ordered by priority list with cars and suppliers.
    """

    priority_to_car: dict = {}

    for history_entry in (
        ShowroomHistory.objects.select_related('car')
        .filter(showroom=showroom, is_active=True)
        .annotate(Count('car'))
    ):
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
    """
    get_unique_showroom_discount: Returns unique discount for showroom if it has it otherwise 1.

    Args:
        showroom (ShowroomModel): Showroom instance.
        supplier (SupplierModel): Supplier instance.

    Returns:
        float: Showroom unique discount.
    """

    if supplier.number_of_sales <= len(showroom.supplier_history.all()):
        return supplier.discount_for_unique_customers
    return 1


def get_supplier_car_with_max_discount(car: CarModel) -> tuple[CarModel, float] | tuple[None, None]:
    """
    get_supplier_car_with_max_discount: Returns cheapest car and discount of that car or None.

    Args:
        car (CarModel): Car instance.

    Returns:
        tuple[CarModel, float]: Car and its discount.
    """

    try:
        discount: SupplierCarDiscount = min(
            SupplierCarDiscount.objects.select_related('supplier').filter(
                cars__pk=car.pk, is_active=True
            ),
            key=lambda discount: discount.precent,
        )

        supplier, max_precent = discount.supplier, discount.precent
        supplier_car: SupplierCar = (
            SupplierCar.objects.select_related('supplier')
            .filter(supplier=supplier, car=car)
            .first()
        )
        return supplier_car, max_precent
    except ValueError:
        return None, None


@shared_task
def buy_supplier_cars() -> None:
    """
    buy_supplier_cars: Buys supplier cars for each showroom.
    """

    for showroom in ShowroomModel.objects.all():
        cars_to_suppliers: list = normalize(showroom)

        cars_with_suppliers_by_priority: list = get_cars_with_suppliers_by_priority(
            showroom, cars_to_suppliers
        )

        for car, supplier in cars_with_suppliers_by_priority:
            supplier_car: SupplierCar = supplier.cars.filter(car=car, is_active=True).first()

            if supplier_car is None:
                return

            unique_showoom_discount: float = get_unique_showroom_discount(showroom, supplier)
            car_with_max_discount, discount = get_supplier_car_with_max_discount(car)

            if (
                car_with_max_discount is None
                or supplier_car.price * unique_showoom_discount
                < car_with_max_discount.price * discount
            ):
                price: float = supplier_car.price * unique_showoom_discount
                chosen_car: SupplierCar = supplier_car
                chosen_supplier: SupplierModel = supplier
            else:
                price = car_with_max_discount.price * discount
                chosen_car = car_with_max_discount
                chosen_supplier = car_with_max_discount.supplier

            if showroom.balance > price:
                showroom_car: ShowroomCar = ShowroomCar.objects.create(
                    car=chosen_car.car,
                    price=price,
                    showroom=showroom,
                    user=None,
                )
                showroom.cars.add(showroom_car)
                showroom.balance -= price
                showroom.save()

                chosen_car.is_active = False
                chosen_car.save()

                history: SupplierHistory = SupplierHistory.objects.create(
                    supplier=chosen_supplier,
                    car=car,
                    sale_price=price,
                    showroom=showroom,
                )
                showroom.supplier_history.add(history)


def get_unique_customer_discount(customer: CustomerModel, showroom: ShowroomModel) -> float:
    """
    get_unique_customer_discount: Returns unique discount for customer if it has it otherwise 1.

    Args:
        customer (CustomerModel): Customer instance.
        showroom (ShowroomModel): Showroom instance.

    Returns:
        float: Customer unique discount.
    """

    if showroom.number_of_sales <= len(customer.showroom_history.all()):
        return showroom.discount_for_unique_customers
    return 1


def get_showroom_car_with_max_discount(car: CarModel) -> tuple[CarModel, float] | tuple[None, None]:
    """
    get_showroom_car_with_max_discount: Returns cheapest car and discount of that car or None.

    Args:
        car (CarModel): Car instance.

    Returns:
        tuple[CarModel, float]: Car and its discount.
    """

    try:
        discount: ShowroomCarDiscount = min(
            ShowroomCarDiscount.objects.select_related('showroom').filter(
                cars__pk=car.pk, is_active=True
            ),
            key=lambda discount: discount.precent,
        )

        showroom, max_precent = discount.showroom, discount.precent
        showroom_car: ShowroomCar = (
            ShowroomCar.objects.select_related('showroom')
            .filter(showroom=showroom, car=car)
            .first()
        )
        return showroom_car, max_precent
    except ValueError:
        return None, None


@shared_task
def make_customer_offer(offer_id: int) -> None:
    """
    make_customer_offer: Buys cars for customer if it has money.

    Args:
        offer (CustomerOffer): CustomerOffer instance.
    """

    offer = CustomerOffer.objects.get(id=offer_id)

    cheapest_car: ShowroomCar = ShowroomCar.objects.filter(car=offer.car, is_active=True).first()

    if not cheapest_car:
        return

    unique_customer_discount: float = get_unique_customer_discount(
        offer.customer, cheapest_car.showroom
    )
    car_with_max_discount, discount = get_showroom_car_with_max_discount(offer.car)

    if (
        car_with_max_discount is None
        or cheapest_car.price * unique_customer_discount < car_with_max_discount.price * discount
    ):
        price: float = cheapest_car.price * unique_customer_discount
        chosen_car: ShowroomCar = cheapest_car
        chosen_showroom: SupplierModel = cheapest_car.showroom
    else:
        price = car_with_max_discount.price * discount
        chosen_car = car_with_max_discount
        chosen_showroom = car_with_max_discount.showroom

    customer = offer.customer

    if offer.max_price > price:
        customer.cars.add(chosen_car)
        customer.balance -= price
        customer.save()

        chosen_car.is_active = False
        chosen_car.save()

        history: ShowroomHistory = ShowroomHistory.objects.create(
            showroom=chosen_showroom,
            car=chosen_car.car,
            sale_price=price,
            customer=customer,
        )
        customer.showroom_history.add(history)

        CustomerHistory.objects.create(
            customer=customer,
            car=chosen_car.car,
            purchase_price=price,
            showroom=chosen_showroom.name,
        )
