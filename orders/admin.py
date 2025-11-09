from django.contrib import admin
from .models import Warehouse, Product, Inventory, Order

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ("product", "warehouse", "quantity", "updated_at")
    list_select_related = ("product", "warehouse")
    search_fields = ("product__name", "warehouse__name")
    list_filter = ("warehouse",)

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ("name", "latitude", "longitude")
    search_fields = ("name",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "units", "status", "assigned_warehouse", "created_at")
    list_select_related = ("product", "assigned_warehouse")
    list_filter = ("status", "assigned_warehouse")
    search_fields = ("product__name",)
