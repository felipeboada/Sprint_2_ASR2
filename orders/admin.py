from django.contrib import admin
from .models import Supplier, Warehouse, Product, Inventory, Order


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'nit', 'email', 'phone', 'city', 'is_active', 'rating']
    list_filter = ['is_active', 'city']
    search_fields = ['name', 'nit', 'email']
    ordering = ['name']


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['product', 'warehouse', 'quantity', 'reserved_quantity', 'updated_at']
    list_select_related = ['product', 'warehouse']
    search_fields = ['product__name', 'warehouse__name']
    list_filter = ['warehouse']


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['name', 'latitude', 'longitude', 'capacity', 'is_active']
    search_fields = ['name', 'address']
    list_filter = ['is_active']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'supplier', 'unit_price', 'is_active']
    search_fields = ['name', 'sku']
    list_filter = ['is_active', 'category', 'supplier']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'customer', 'units', 'status', 'assigned_warehouse', 'created_at']
    list_select_related = ['product', 'assigned_warehouse', 'customer']
    list_filter = ['status', 'created_at']
    search_fields = ['product__name', 'customer__username']
