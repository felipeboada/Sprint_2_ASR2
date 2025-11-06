from django.db import models



class Warehouse(models.Model):  # representa una bodega física

    name= models.CharField(max_length=100, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='inventories')

    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='inventories', null=True, blank=True)

    quantity = models.PositiveIntegerField(default=0)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:


        verbose_name_plural = "Inventory"
        unique_together = [('product','warehouse')]

        indexes = [models.Index(fields=['product','quantity']), models.Index(fields=['warehouse'])]

    
    def __str__(self):
        wn = self.warehouse.name if self.warehouse else "N/A"
        return f"{self.product.name} @ {wn} — {self.quantity} u"

class Order(models.Model):
    PENDING='PENDING'; CONFIRMED='CONFIRMED'; REJECTED='REJECTED'

    STATUS_CHOICES=[(PENDING,'Pending'),(CONFIRMED,'Confirmed'),(REJECTED,'Rejected')]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')

    units = models.PositiveIntegerField()

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)

    assigned_warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:

        indexes = [models.Index(fields=['product','status'])]
        
    def __str__(self): return f"Order #{self.id} {self.product.name} x{self.units} [{self.status}]" # representación legible de la orden




from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Order)
def update_inventory_on_confirm(sender, instance, **kwargs):
    if instance.status == Order.CONFIRMED:
        try:
            inventory = Inventory.objects.get(product=instance.product, warehouse=instance.assigned_warehouse)
            inventory.quantity = max(inventory.quantity - instance.units, 0)
            inventory.save()
        except Inventory.DoesNotExist:
            pass
