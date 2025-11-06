from django.contrib import admin
from .models import Product, Order, Inventory, Warehouse

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Inventory)
admin.site.register(Warehouse)
