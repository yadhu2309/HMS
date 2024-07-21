from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class InventorySerializer(serializers.ModelSerializer):
    item = serializers.ReadOnlyField(source='menu_items.name')
    class Meta:
        model = Inventory
        fields = '__all__'

class InventoryDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['quantity_in_stock']

class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    inventory_items = InventoryDataSerializer(many=True, read_only=True)

    # first_inventory_item =InventoryDataSerializer(read_only=True)
    class Meta:
        model = MenuItem
        fields = '__all__'
    

class OrderItemSerializer(serializers.ModelSerializer):
    menu_items = MenuItemSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'menu_items', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ['table_number', 'status', 'total_price', 'order_time', 'items']
    

