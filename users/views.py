from django.shortcuts import redirect
from requests import Response
from rest_framework import generics, permissions
from .models import User
from .serializers import UserSerializer
from django.contrib.auth.decorators import login_required

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    from rest_framework.decorators import api_view, permission_classes
    from rest_framework.permissions import IsAuthenticated
    from rest_framework.response import Response

    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def role_dashboard(request):
        user = request.User
        role = user.role

        if role == 'gm':
            # Add logic to fetch data GM needs (e.g., pending approvals)
            return Response({"role": "General Manager", "message": "GM dashboard data here"})

        elif role == 'warehouse_manager':
            return Response({"role": "Warehouse Manager", "message": "Warehouse dashboard data"})

        elif role == 'cashier':
            return Response({"role": "Cashier", "message": "Cashier dashboard data"})

        elif role == 'cse':
            return Response({"role": "CSE", "message": "CSE dashboard data"})

        elif role == 'delivery_boy':
            return Response({"role": "Delivery Boy", "message": "Delivery dashboard data"})

        else:
            return Response({"error": "Unknown role"}, status=400)

