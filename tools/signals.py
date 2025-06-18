from django.dispatch import receiver
from borrow.signals import request_approved
from .models import Tool

@receiver(request_approved)
def handle_request_approved(sender, **kwargs):
    """
    Listen for an approved request and update the tool's availability.
    """
    rental_request = kwargs['borrow_request']
    tool = rental_request.tool
    tool.availability_status = Tool.Availability.BORROWED
    tool.save()

    print(f"Signal received: Tool '{tool.name}' status set to Borrowed.")