from ..models import Measurement
from orders.logic import restock_atomic, get_inventory

def get_measurements():
    # Return latest inventories for UI stock page
    from orders.models import Inventory
    queryset = Inventory.objects.select_related('product').all().order_by('product__name')
    return queryset


def create_measurement(form):
    measurement = form.save(commit=False)
    variable = measurement.variable
    units = int(measurement.value or 0)
    # Perform atomic restock tied to product name
    inv = restock_atomic(variable.name, units)
    # Link measurement to product for auditing and save
    measurement.product_id = inv.product_id
    measurement.save()
    return ()