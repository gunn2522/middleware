from django.urls import path

from approvals import views
from .views import UserListCreateView ,

urlpatterns = [
    path('list-create/', UserListCreateView.as_view(), name='user-list-create'),

    path('dashboard/', views.role_based_redirect, name='role_redirect'),
    path('dashboard/gm/', views.gm_dashboard, name='gm_dashboard'),
    path('dashboard/warehouse/', views.warehouse_dashboard, name='warehouse_dashboard'),
    path('dashboard/cashier/', views.cashier_dashboard, name='cashier_dashboard'),
    path('dashboard/cse/', views.cse_dashboard, name='cse_dashboard'),
    path('dashboard/delivery/', views.delivery_dashboard, name='delivery_dashboard'),
]
