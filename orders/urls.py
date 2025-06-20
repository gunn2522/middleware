from django.contrib import admin
from django.urls import path
from orders.views import OrderCreateAPI, health_check, empty_favicon

urlpatterns = [
    path('', health_check),
    path('favicon.ico', empty_favicon),
    path('api/orders/create/', OrderCreateAPI.as_view()),
    path('admin/', admin.site.urls),
]
