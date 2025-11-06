from rest_framework import serializers
from .models import Product, Inventory, Order, Warehouse



class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id', 'name', 'latitude', 'longitude']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name']


class InventorySerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    warehouse = WarehouseSerializer()

    class Meta:
        model = Inventory
        fields = ['product', 'warehouse', 'quantity', 'updated_at']


class OrderSerializer(serializers.ModelSerializer):
    
    product = ProductSerializer()
    assigned_warehouse = WarehouseSerializer()

    class Meta:
        model = Order
        fields = ['id', 'product', 'units', 'status', 'assigned_warehouse', 'created_at']
