# klub_chat/routing.py

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # 채팅방 WebSocket
    re_path(
        r'ws/chat/(?P<room_name>[\w-]+)/$',
        consumers.ChatConsumer.as_asgi()
    ),

    # 미팅 알람 WebSocket
    re_path(
        r'ws/meeting-alerts/$',
        consumers.MeetingAlertConsumer.as_asgi()
    ),
]
