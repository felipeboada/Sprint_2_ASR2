from django.db import models
from orders.models import Warehouse
from products.models import Variable

class Measurement(models.Model):
    variable = models.ForeignKey(Variable, on_delete=models.CASCADE, default=None)
    value = models.FloatField(null=True, blank=True, default=None)
    unit = models.CharField(max_length=50)
    dateTime = models.DateTimeField(auto_now_add=True)
    place= models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    product = models.ForeignKey('orders.Product', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return '%s %s' % (self.value, self.unit)