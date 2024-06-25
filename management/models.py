from typing import Iterable
from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    preparation_time = models.IntegerField()
    available = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='menu_items')

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Preparation', 'In Preparation'),
        ('Ready', 'Ready'),
        ('Served', 'Served'),
        ('Cancelled', 'Cancelled')
    ]
    table_number = models.IntegerField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending') 
    order_time = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_items = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    sub_total = models.DecimalField(max_digits=8, decimal_places=2)

    def save(self, *args, **kwargs):
        self.sub_total = self.menu_items.price * self.quantity
        return super().save(*args, **kwargs)
    
class Inventory(models.Model):
    menu_items = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity_in_stock = models.IntegerField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.quantity_in_stock > 0:
            self.menu_items.available = True
        else:
            self.menu_items.available = False
        self.menu_items.save()
