import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# Import routing from BOTH of your apps
import messaging.routing
import core.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sajhatools.settings')

# Combine the websocket URL patterns from all apps into one list
combined_patterns = messaging.routing.websocket_urlpatterns + core.routing.websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # Update the websocket router to use the combined list of patterns
    "websocket": AuthMiddlewareStack(
        URLRouter(
            combined_patterns
        )
    ),
})