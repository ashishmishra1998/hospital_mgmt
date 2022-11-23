from django.urls import re_path
from . import consumers


websocket_urlpatterns = [
    re_path(r'ws/socket-server/', consumers.NotificationConsumer.as_asgi()),
    re_path(r'ws/socket-notification/', consumers.NotificationConsumerSocket.as_asgi())
]