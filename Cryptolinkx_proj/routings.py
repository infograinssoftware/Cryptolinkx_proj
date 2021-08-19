import os
# import django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
from core.consumers import ExchangeConsumer, P2PConsumer
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Cryptolinkx_proj.settings")
# django.setup()

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/exchange/", ExchangeConsumer.as_asgi()),
            path("ws/p2p/", P2PConsumer.as_asgi()),
            path("ws/p2p/<str:pair_name>", P2PConsumer.as_asgi()),
        ])
    ),
})
