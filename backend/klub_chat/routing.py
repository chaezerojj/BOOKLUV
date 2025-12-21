# klub_chat/routing.py

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # 채팅방에 대한 WebSocket URL
    re_path(r'ws/chat/(?P<room_name>[\w-]+)/$', consumers.ChatConsumer.as_asgi()),

    # 미팅 알람에 대한 WebSocket URL
    re_path(r'ws/meeting-alerts/$', consumers.MeetingAlertConsumer.as_asgi()),
]
