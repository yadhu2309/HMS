from django.db import transaction
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db.models import Prefetch

from .models import Category, MenuItem, Order, OrderItem, Inventory
from .serializer import *
# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all().select_related('category').prefetch_related('inventory_items')
    # queryset = MenuItem.objects.select_related('category').prefetch_related(
    #     Prefetch('inventory_items', queryset=Inventory.objects.order_by('id'))
    # ).all()
    serializer_class = MenuItemSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().prefetch_related('items__menu_items')
    serializer_class = OrderSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
    
        order_items = request.data.get('order_items', [])
        if not order_items:
            raise ValidationError('No order items provided.')
        order = serializer.save()
        total_price = 0
        for item in order_items:
            try:
                menu_item = MenuItem.objects.get(id=item['menu_item'])
            except:
                raise ValidationError(f"Menu item not found for ID {item['menu_item']}")
            if not menu_item.available:
                raise ValidationError(f"Menu item {menu_item.name} is not available.")
            print(menu_item.name)
            inventory_item = Inventory.objects.get(menu_items=menu_item)
            print(inventory_item)
            if inventory_item.quantity_in_stock < item['quantity']:
                raise ValidationError(f'Not enough {menu_item.name} in inventory.')

            OrderItem.objects.create(order=order, quantity=item['quantity'], menu_items=menu_item)
            total_price += item['quantity'] * menu_item.price

            # inventory_item.quantity_in_stock -= item['quantity']
            # inventory_item.save()
            inventory_item.update_quantity_in_stock(item['quantity'])

            if inventory_item.quantity_in_stock <= 0:
                menu_item = inventory_item.menu_items
                menu_item.available = False
                menu_item.save()
                inventory_item.delete()
            
        order.total_price = total_price
        order.save()
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)
    
class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all().select_related('menu_items')
    serializer_class = InventorySerializer
