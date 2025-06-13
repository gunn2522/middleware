from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


def is_approved(self):
    return hasattr(self, 'approval') and self.approval.status == 'approved'

# Master list of warehouses
class Warehouse(models.Model):
    name = models.CharField(max_length=100, unique=True)


    def __str__(self):
        return self.name


# Master list of vehicles
class Vehicle(models.Model):
    vehicle_number = models.CharField(max_length=50, unique=True)


    def __str__(self):
        return self.vehicle_number


# Master list of items
class Item(models.Model):
    ITEM_TYPES = [
        ('refill', 'Refill Cylinder'),
        ('nfr', 'Non-Fuel Item'),
        ('sv', 'Subscription Voucher'),
        ('tv', 'Termination Voucher'),
    ]
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=ITEM_TYPES)
    stock = models.PositiveIntegerField(default=0)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.stock} in {self.warehouse.name})"


# Orders model
class Order(models.Model):
    ORDER_TYPES = [
        ('refill', 'Refill'),
        ('nfr', 'Non-Fuel Item'),
        ('sv', 'Subscription Voucher'),
        ('tv_in', 'TV In'),
        ('tv_out', 'TV Out'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
        ('collected', 'Collected'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_type = models.CharField(max_length=20, choices=ORDER_TYPES)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveIntegerField()
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, blank=True, null=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, blank=True, null=True)
    virtual_code = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name='approved_orders',
        on_delete=models.SET_NULL
    )
    justification = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_order_type_display()} - {self.item.name if self.item else 'No Item'} x{self.quantity} ({self.status})"

    def clean(self):
        if self.item and self.warehouse:
            # Ensure warehouse matches item
            if self.item.warehouse != self.warehouse:
                raise ValidationError("Selected item is not available in the chosen warehouse.")

            # Check stock
            if self.quantity > self.item.stock:
                raise ValidationError(f"Not enough stock for {self.item.name}. Only {self.item.stock} available.")

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        self.full_clean()
        super().save(*args, **kwargs)

        # Deduct stock only for new pending orders
        if is_new and self.status == 'pending' and self.item:
            self.item.stock -= self.quantity
            self.item.save()
