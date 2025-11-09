from ..models import Variable
from orders.logic import create_or_get_product

def get_variables():
    queryset = Variable.objects.all()
    return (queryset)


def create_variable(form):
    variable = form.save()
    # Link Variable to Orders.Product and ensure inventory exists
    product = create_or_get_product(variable.name)
    variable.product = product
    variable.save(update_fields=['product'])
    return ()