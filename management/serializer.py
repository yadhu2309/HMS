from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class MenuItemSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
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
    
class InventorySerializer(serializers.ModelSerializer):
    item = serializers.ReadOnlyField(source='menu_items.name')
    class Meta:
        model = Inventory
        fields = '__all__'

