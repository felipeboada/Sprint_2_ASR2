from typing import Tuple
from django.db import transaction, DatabaseError
from django.db.models import F
from .models import Inventory, Order, Product


def create_or_get_product(name: str) -> Product:
    product, _ = Product.objects.get_or_create(name=name)
    Inventory.objects.get_or_create(product=product)
    return product


def place_order_atomic(product_name: str, units: int, max_retries: int = 3) -> Tuple[Order, bool]:
    """Place an order and atomically decrement inventory if available.
    Returns (order, confirmed_flag). Uses SELECT ... FOR UPDATE to avoid lost updates.
    """
    if units <= 0:
        raise ValueError("units must be > 0")

    product = create_or_get_product(product_name)

    attempt = 0
    while True:
        attempt += 1
        try:
            with transaction.atomic():
                inventory = (
                    Inventory.objects.select_for_update()
                    .select_related('product')
                    .get(product=product)
                )

                order = Order.objects.create(product=product, units=units)

                if inventory.quantity >= units:
                    # Safe in-row update
                    Inventory.objects.filter(pk=inventory.pk, quantity__gte=units).update(
                        quantity=F('quantity') - units
                    )
                    order.status = Order.CONFIRMED
                    order.save(update_fields=['status'])
                    return order, True
                else:
                    order.status = Order.REJECTED
                    order.save(update_fields=['status'])
                    return order, False
        except DatabaseError:
            if attempt >= max_retries:
                raise
            continue


def restock_atomic(product_name: str, units: int) -> Inventory:
    if units <= 0:
        raise ValueError("units must be > 0")
    product = create_or_get_product(product_name)
    with transaction.atomic():
        inventory = (
            Inventory.objects.select_for_update()
            .select_related('product')
            .get(product=product)
        )
        Inventory.objects.filter(pk=inventory.pk).update(quantity=F('quantity') + units)
        inventory.refresh_from_db()
        return inventory


def get_inventory(product_name: str) -> Inventory:
    product = create_or_get_product(product_name)
    return Inventory.objects.select_related('product').get(product=product)
