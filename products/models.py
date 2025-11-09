from django.db import models
from django.db import models

class Variable(models.Model):
    name = models.CharField(max_length=50)
    # Bridge field to the new Product domain entity
    product = models.ForeignKey('orders.Product', on_delete=models.CASCADE, null=True, blank=True, related_name='legacy_variables')

    def __str__(self):
        return '{}'.format(self.name)

