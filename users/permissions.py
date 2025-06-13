from rest_framework.permissions import BasePermission

class IsManagerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in ['GET', 'HEAD', 'OPTIONS'] or
            request.user.role in ['warehouse_manager', 'gm']
        )

