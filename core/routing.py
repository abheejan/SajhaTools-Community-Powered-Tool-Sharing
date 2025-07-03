from django.urls import path
from .consumers import NotificationConsumer

websocket_urlpatterns = [
    # This URL is what our frontend will connect to.
    path('ws/notifications/', NotificationConsumer.as_asgi()),
]