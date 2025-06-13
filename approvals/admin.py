# approvals/admin.py

from django.contrib import admin
from .models import Approval

@admin.register(Approval)
class ApprovalAdmin(admin.ModelAdmin):
    list_display = ['order', 'approved_by', 'status', 'timestamp']
    search_fields = ['order__id', 'approved_by__username', 'status']
    list_filter = ['status', 'timestamp']
