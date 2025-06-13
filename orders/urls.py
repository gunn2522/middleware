# orders/urls.py

from django.urls import path
from .api_views import (
    OrderListCreateAPIView, OrderDetailAPIView,
    WarehouseListAPIView, ItemListAPIView, VehicleListAPIView
)

urlpatterns = [
    path('orders/', OrderListCreateAPIView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail'),
    path('warehouses/', WarehouseListAPIView.as_view(), name='warehouse-list'),
    path('items/', ItemListAPIView.as_view(), name='item-list'),
    path('vehicles/', VehicleListAPIView.as_view(), name='vehicle-list'),
]
