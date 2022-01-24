from django.urls import re_path

from . import cunsumers

websocket_urlpatterns = [
    re_path(r'', cunsumers.ChatConsumer.as_asgi())
]