from django.contrib import admin
from django.utils.html import format_html
from .models import Measurement


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_info', 'warehouse_info', 'quantity_display', 'measurement_type', 'created_at']
    list_filter = ['created_at']
    search_fields = ['product__name', 'warehouse__name']
    ordering = ['-created_at']
    list_per_page = 30
    date_hierarchy = 'created_at'
    
    @admin.display(description='Producto')
    def product_info(self, obj):
        if hasattr(obj, 'product') and obj.product:
            return format_html(f'📦 <b>{obj.product.name}</b>')
        return format_html('<span style="color: #6c757d;">-</span>')
    
    @admin.display(description='Bodega')
    def warehouse_info(self, obj):
        if hasattr(obj, 'warehouse') and obj.warehouse:
            return format_html(f'📍 {obj.warehouse.name}')
        return format_html('<span style="color: #6c757d;">-</span>')
    
    @admin.display(description='Cantidad', ordering='quantity')
    def quantity_display(self, obj):
        if hasattr(obj, 'quantity'):
            color = '#28a745' if obj.quantity > 0 else '#dc3545'
            return format_html(f'<span style="color: {color};"><b>{obj.quantity}</b> unidades</span>')
        return format_html('<span style="color: #6c757d;">-</span>')
    
    @admin.display(description='Tipo')
    def measurement_type(self, obj):
        return format_html('<span style="background-color: #E1F5FE; padding: 3px 10px; border-radius: 3px;">Medición</span>')
