from django.db import models
from django.conf import settings
from tools.models import Tool

class BorrowRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        DENIED = 'denied', 'Denied'
        CANCELLED = 'cancelled', 'Cancelled'
        COMPLETED = 'completed', 'Completed'

    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='borrow_requests')
    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )
    request_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    # Timestamps for status changes
    approved_date = models.DateTimeField(null=True, blank=True)
    denied_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Request for '{self.tool.name}' by {self.borrower.username} ({self.get_status_display()})"