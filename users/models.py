# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.Model):
    ROLE_CHOICES = (
        ('cashier', 'Cashier'),
        ('warehouse_manager', 'Warehouse Manager'),
        ('delivery_boy', 'Delivery Boy'),
        ('cse', 'Customer Service Executive'),
        ('gm', 'General Manager'),
    )
    name = models.CharField(max_length=50, choices=ROLE_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()

class User(AbstractUser):
    roles = models.ManyToManyField(Role, related_name='users')

    def has_role(self, role_name):
        return self.roles.filter(name=role_name).exists()

