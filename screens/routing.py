from django.urls import re_path

from .consumers import ChatConsumer, ScreenConsumer

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
    re_path(r"ws/screen/(?P<screen_id>\w+)/$", ScreenConsumer.as_asgi()),
]