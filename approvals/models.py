# approvals/models.py

from django.db import models
from django.conf import settings
from orders.models import Order

class Approval(models.Model):
    APPROVAL_STATUS = [
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='approval')
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=APPROVAL_STATUS)
    justification = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order} - {self.status} by {self.approved_by}"
