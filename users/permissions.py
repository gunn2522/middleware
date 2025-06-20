from rest_framework.permissions import BasePermission

class IsCashier(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'cashier'

class IsWarehouseManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'warehouse_manager'

class IsDeliveryBoy(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'delivery_boy'

class IsCustomerServiceExecutive(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'customer_service_executive'
