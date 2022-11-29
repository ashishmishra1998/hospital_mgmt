"""
ASGI config for hospital_mgmt project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
import hospital.routing
import django


# from django.core.asgi import get_asgi_application
from channels.routing import get_default_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import hospital.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_mgmt.settings')

django.setup()

application = ProtocolTypeRouter({
    'http':get_default_application(),
    'websocket':AuthMiddlewareStack(
        URLRouter(
            hospital.routing.websocket_urlpatterns
        )
    )
})

application = get_default_application()
