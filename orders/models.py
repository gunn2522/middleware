from datetime import date

from django.db import models

class Order(models.Model):
    ORDER_TYPES = [
        ('refill', 'Refill'),
        ('NFR', 'Non-Fuel Refill'),
    ]

    order_type = models.CharField(max_length=10, choices=ORDER_TYPES)
    vehicle_number = models.CharField(max_length=20)
    warehouse = models.CharField(max_length=100)
    item = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    delivery_address = models.TextField()
    delivery_date = models.DateField(default=date.today)  # ✅ default = today

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.order_type} - {self.item}"
