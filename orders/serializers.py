from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import Product, Inventory, Order, Warehouse, Supplier


class SupplierSerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Supplier
        fields = [
            'id', 'name', 'nit', 'email', 'phone', 'address', 'city',
            'contact_person', 'is_active', 'credit_days', 'rating',
            'notes', 'products_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'products_count']
    
    def get_products_count(self, obj):
        return obj.products.count()
    
    def validate(self, data):
        try:
            if self.instance:
                supplier = self.instance
                for key, value in data.items():
                    setattr(supplier, key, value)
            else:
                supplier = Supplier(**data)
            supplier.clean()
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        return data


class WarehouseSerializer(serializers.ModelSerializer):
    current_stock = serializers.SerializerMethodField()
    available_capacity = serializers.SerializerMethodField()
    
    class Meta:
        model = Warehouse
        fields = [
            'id', 'name', 'latitude', 'longitude', 'address', 'phone',
            'capacity', 'is_active', 'current_stock', 'available_capacity',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'current_stock', 'available_capacity']
    
    def get_current_stock(self, obj):
        return obj.get_current_stock()
    
    def get_available_capacity(self, obj):
        return obj.get_available_capacity()
    
    def validate(self, data):
        try:
            if self.instance:
                warehouse = self.instance
                for key, value in data.items():
                    setattr(warehouse, key, value)
            else:
                warehouse = Warehouse(**data)
            warehouse.clean()
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        return data


class ProductSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    total_stock = serializers.SerializerMethodField()
    profit_margin = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'sku', 'supplier', 'supplier_name',
            'unit_price', 'cost_price', 'category', 'min_stock', 'max_stock',
            'is_active', 'requires_special_handling', 'total_stock',
            'profit_margin', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'total_stock', 'profit_margin']
    
    def get_total_stock(self, obj):
        return obj.get_total_stock()
    
    def get_profit_margin(self, obj):
        return round(obj.get_profit_margin(), 2)
    
    def validate(self, data):
        try:
            if self.instance:
                product = self.instance
                for key, value in data.items():
                    setattr(product, key, value)
            else:
                product = Product(**data)
            product.clean()
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        return data


class InventorySerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)
    available_quantity = serializers.SerializerMethodField()
    
    class Meta:
        model = Inventory
        fields = [
            'id', 'product', 'product_name', 'warehouse', 'warehouse_name',
            'quantity', 'reserved_quantity', 'available_quantity',
            'updated_at', 'last_restock_date'
        ]
        read_only_fields = ['updated_at', 'available_quantity']
    
    def get_available_quantity(self, obj):
        return obj.get_available_quantity()
    
    def validate(self, data):
        try:
            if self.instance:
                inventory = self.instance
                for key, value in data.items():
                    setattr(inventory, key, value)
            else:
                inventory = Inventory(**data)
            inventory.clean()
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        return data


class OrderSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    warehouse_name = serializers.CharField(source='assigned_warehouse.name', read_only=True)
    customer_name = serializers.CharField(source='customer.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'product', 'product_name', 'units', 'status', 'status_display',
            'assigned_warehouse', 'warehouse_name', 'customer', 'customer_name',
            'delivery_address', 'delivery_zone', 'total_price', 'notes',
            'created_at', 'updated_at', 'confirmed_at', 'delivered_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'confirmed_at', 'delivered_at']
    
    def validate(self, data):
        try:
            if self.instance:
                order = self.instance
                for key, value in data.items():
                    setattr(order, key, value)
            else:
                order = Order(**data)
            order.clean()
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        return data
