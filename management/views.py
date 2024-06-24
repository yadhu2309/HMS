from django.shortcuts import render
from django.db import transaction
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .models import Category, MenuItem, Order, OrderItem
from .serializer import CategorySerializer, MenuItemSerializer, OrderSerializer
# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
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
                raise ValidationError(f'Menu item with id {item["menu_item"]} does not exist.')
            
            OrderItem.objects.create(order=order, quantity=item['quantity'], menu_items=menu_item)
            total_price += item['quantity'] * menu_item.price
        order.total_price = total_price
        order.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)