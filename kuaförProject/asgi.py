"""
ASGI config for kuaförProject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
import kuaförApp.routing
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kuaförProject.settings")

application = get_asgi_application()
application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    'websocket':AuthMiddlewareStack(
            URLRouter(
                kuaförApp.routing.websocket_urlpatterns
            )
    )
})