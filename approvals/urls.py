from django.urls import path
from .views import approve_order, reject_order

urlpatterns = [
    path('approve/<int:order_id>/', approve_order, name='approve_order'),
    path('reject/<int:order_id>/', reject_order, name='reject_order'),
    path('dashboard/', manager_dashboard, name='manager_dashboard'),

]
