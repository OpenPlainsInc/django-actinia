"""
ASGI config for api project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

from multiprocessing.spawn import import_main_path
import os
import django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from django.core.asgi import get_asgi_application
import grass.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_api.settings")

# application = get_asgi_application()
ws_url_patters = []
ws_url_patters.extend(grass.routing.websocket_urlpatterns)

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        # Just HTTP for now. (We can add other protocols later.)
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(ws_url_patters))
        ),
    }
)
