from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from . import consumers

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    path("ws/siparis_durumu/", consumers.SiparisDurumuConsumer.as_asgi()),
    # path("ws/siparis_geldi/", consumers.SiparisGeldiConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
    # Diğer protokoller için gerekli yapılandırmaları buraya ekleyin
})