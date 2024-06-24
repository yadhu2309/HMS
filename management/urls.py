from django.urls import path, include
from .views import CategoryViewSet, MenuItemViewSet, OrderViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'category', CategoryViewSet)
router.register(r'menu-item', MenuItemViewSet)
router.register(r'order', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]