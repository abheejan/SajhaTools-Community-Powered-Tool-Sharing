from django.db import models
from django.conf import settings
from django.urls import reverse

class Tool(models.Model):
    class Availability(models.TextChoices):
        AVAILABLE = 'available', 'Available'
        BORROWED = 'borrowed', 'Borrowed'

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='tool_images/', default='tool_images/default.jpg')
    availability_status = models.CharField(
        max_length=10,
        choices=Availability.choices,
        default=Availability.AVAILABLE
    )
    pickup_address = models.CharField(max_length=255)
    posted_time = models.DateTimeField(auto_now_add=True)
    preferred_pickup_time = models.CharField(max_length=100, help_text="e.g., Weekdays after 5 PM")

    def __str__(self):
        return f"{self.name} owned by {self.owner.username}"

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this tool."""
        return reverse('tool-detail', args=[str(self.id)])