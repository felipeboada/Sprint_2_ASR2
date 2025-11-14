from django.contrib import admin
from django.utils.html import format_html
from .models import Supplier, Warehouse, Product, Inventory, Order


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'nit', 'email', 'phone', 'city', 'status_badge', 'rating_stars']
    list_filter = ['is_active', 'city', 'rating']
    search_fields = ['name', 'nit', 'email', 'contact_person']
    ordering = ['-rating', 'name']
    list_per_page = 25
    
    fieldsets = (
        ('Información General', {
            'fields': ('name', 'nit', 'email', 'phone')
        }),
        ('Ubicación', {
            'fields': ('address', 'city')
        }),
        ('Contacto y Evaluación', {
            'fields': ('contact_person', 'rating', 'credit_days')
        }),
        ('Estado', {
            'fields': ('is_active', 'notes')
        }),
    )
    
    @admin.display(description='Estado', ordering='is_active')
    def status_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="color: white; background-color: #28a745; padding: 3px 10px; border-radius: 3px;">✓ Activo</span>')
        return format_html('<span style="color: white; background-color: #dc3545; padding: 3px 10px; border-radius: 3px;">✗ Inactivo</span>')
    
    @admin.display(description='Calificación')
    def rating_stars(self, obj):
        stars = '⭐' * int(obj.rating) if obj.rating else '☆☆☆☆☆'
        return format_html(f'<span style="font-size: 16px;">{stars}</span>')


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['name', 'city_location', 'capacity_info', 'stock_level', 'status_badge']
    search_fields = ['name', 'address']
    list_filter = ['is_active']
    list_per_page = 20
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'is_active')
        }),
        ('Ubicación', {
            'fields': ('address', 'phone', 'latitude', 'longitude'),
            'description': 'Coordenadas GPS para optimización de rutas'
        }),
        ('Capacidad', {
            'fields': ('capacity',)
        }),
    )
    
    @admin.display(description='Ubicación')
    def city_location(self, obj):
        return format_html(f'📍 {obj.address or "No especificada"}')
    
    @admin.display(description='Capacidad')
    def capacity_info(self, obj):
        return format_html(f'<b>{obj.capacity:,}</b> unidades')
    
    @admin.display(description='Ocupación')
    def stock_level(self, obj):
        current = obj.get_current_stock()
        percentage = (current / obj.capacity * 100) if obj.capacity > 0 else 0
        color = '#28a745' if percentage < 70 else '#ffc107' if percentage < 90 else '#dc3545'
        return format_html(
            f'<div style="width: 100px; background-color: #e9ecef; border-radius: 3px;">'
            f'<div style="width: {percentage}%; background-color: {color}; color: white; padding: 2px; border-radius: 3px; text-align: center;">'
            f'{percentage:.0f}%</div></div>'
        )
    
    @admin.display(description='Estado', ordering='is_active')
    def status_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="color: white; background-color: #28a745; padding: 3px 10px; border-radius: 3px;">✓ Activo</span>')
        return format_html('<span style="color: white; background-color: #dc3545; padding: 3px 10px; border-radius: 3px;">✗ Inactivo</span>')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'supplier', 'price_display', 'stock_status', 'status_badge']
    search_fields = ['name', 'sku', 'description']
    list_filter = ['is_active', 'category', 'supplier', 'requires_special_handling']
    ordering = ['name']
    list_per_page = 25
    
    fieldsets = (
        ('Información del Producto', {
            'fields': ('name', 'description', 'sku', 'category')
        }),
        ('Proveedor', {
            'fields': ('supplier',)
        }),
        ('Precios', {
            'fields': ('cost_price', 'unit_price'),
            'description': 'El precio de venta debe ser mayor al precio de costo'
        }),
        ('Inventario', {
            'fields': ('min_stock', 'max_stock')
        }),
        ('Configuración', {
            'fields': ('is_active', 'requires_special_handling')
        }),
    )
    
    @admin.display(description='Precio', ordering='unit_price')
    def price_display(self, obj):
        profit = obj.get_profit_margin()
        color = '#28a745' if profit > 30 else '#ffc107' if profit > 15 else '#dc3545'
        return format_html(
            f'<b>${obj.unit_price:,.0f}</b><br>'
            f'<small style="color: {color};">Margen: {profit:.1f}%</small>'
        )
    
    @admin.display(description='Stock Total')
    def stock_status(self, obj):
        total = obj.get_total_stock()
        if total == 0:
            color = '#dc3545'
            icon = '⚠️'
        elif total < obj.min_stock:
            color = '#ffc107'
            icon = '⚡'
        else:
            color = '#28a745'
            icon = '✓'
        return format_html(f'<span style="color: {color};"><b>{icon} {total}</b> unidades</span>')
    
    @admin.display(description='Estado', ordering='is_active')
    def status_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="color: white; background-color: #28a745; padding: 3px 10px; border-radius: 3px;">✓ Activo</span>')
        return format_html('<span style="color: white; background-color: #dc3545; padding: 3px 10px; border-radius: 3px;">✗ Inactivo</span>')


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['product', 'warehouse', 'quantity_display', 'reserved_display', 'available_display', 'updated_at']
    list_select_related = ['product', 'warehouse']
    search_fields = ['product__name', 'warehouse__name']
    list_filter = ['warehouse', 'updated_at']
    list_per_page = 30
    
    @admin.display(description='Cantidad Total', ordering='quantity')
    def quantity_display(self, obj):
        return format_html(f'<b>{obj.quantity}</b> unidades')
    
    @admin.display(description='Reservado', ordering='reserved_quantity')
    def reserved_display(self, obj):
        if obj.reserved_quantity > 0:
            return format_html(f'<span style="color: #ffc107;"><b>{obj.reserved_quantity}</b> unidades</span>')
        return format_html('<span style="color: #6c757d;">0</span>')
    
    @admin.display(description='Disponible')
    def available_display(self, obj):
        available = obj.get_available_quantity()
        color = '#28a745' if available > 0 else '#dc3545'
        return format_html(f'<span style="color: {color};"><b>{available}</b> unidades</span>')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'customer_info', 'product', 'units', 'status_badge', 'warehouse_info', 'price_display', 'created_at']
    list_select_related = ['product', 'assigned_warehouse', 'customer']
    list_filter = ['status', 'created_at', 'assigned_warehouse']
    search_fields = ['id', 'product__name', 'customer__username', 'customer__first_name', 'customer__last_name']
    ordering = ['-created_at']
    list_per_page = 30
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Información del Pedido', {
            'fields': ('product', 'units', 'status')
        }),
        ('Cliente', {
            'fields': ('customer', 'delivery_address', 'delivery_zone')
        }),
        ('Asignación', {
            'fields': ('assigned_warehouse',)
        }),
        ('Precio', {
            'fields': ('total_price',)
        }),
        ('Notas', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
    
    @admin.display(description='Pedido #', ordering='id')
    def order_id(self, obj):
        return format_html(f'<b>#{obj.id}</b>')
    
    @admin.display(description='Cliente', ordering='customer__username')
    def customer_info(self, obj):
        if obj.customer:
            name = obj.customer.get_full_name() or obj.customer.username
            role = obj.customer.get_role_display()
            return format_html(f'<b>{name}</b><br><small>{role}</small>')
        return '-'
    
    @admin.display(description='Estado', ordering='status')
    def status_badge(self, obj):
        colors = {
            'PENDING': '#ffc107',
            'CONFIRMED': '#28a745',
            'REJECTED': '#dc3545',
            'CANCELLED': '#6c757d',
            'IN_TRANSIT': '#17a2b8',
            'DELIVERED': '#20c997',
        }
        icons = {
            'PENDING': '⏳',
            'CONFIRMED': '✓',
            'REJECTED': '✗',
            'CANCELLED': '⊘',
            'IN_TRANSIT': '🚚',
            'DELIVERED': '📦',
        }
        color = colors.get(obj.status, '#6c757d')
        icon = icons.get(obj.status, '•')
        return format_html(
            f'<span style="color: white; background-color: {color}; padding: 3px 10px; border-radius: 3px;">'
            f'{icon} {obj.get_status_display()}</span>'
        )
    
    @admin.display(description='Bodega', ordering='assigned_warehouse__name')
    def warehouse_info(self, obj):
        if obj.assigned_warehouse:
            return format_html(f'📍 {obj.assigned_warehouse.name}')
        return format_html('<span style="color: #6c757d;">Sin asignar</span>')
    
    @admin.display(description='Total', ordering='total_price')
    def price_display(self, obj):
        return format_html(f'<b>${obj.total_price:,.0f}</b>')
