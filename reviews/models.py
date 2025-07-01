from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from borrow.models import BorrowRequest

class Review(models.Model):
    rental_request = models.OneToOneField(
        BorrowRequest,
        on_delete=models.CASCADE,
        related_name='review'
    )
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.rental_request.tool.name} - {self.rating} stars"

    class Meta:
        ordering = ['-created_at']