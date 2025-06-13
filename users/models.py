from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
    ('delivery_boy', 'Delivery Boy'),
    ('cse', 'Customer Service Executive'),
    ('cashier', 'Cashier'),
    ('warehouse_manager', 'Warehouse Manager'),
    ('gm', 'General Manager'),
]
    role = models.CharField(max_length=30, choices= ROLE_CHOICES)

def __str__(self):
    return f"{self.username} ({self.get_role_display()})"
