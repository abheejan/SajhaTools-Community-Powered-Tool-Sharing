from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    # The URL matches the WebSocket connection address in our JavaScript
    path('ws/chat/<int:thread_id>/', ChatConsumer.as_asgi()),
]