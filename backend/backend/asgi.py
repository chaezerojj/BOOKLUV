# asgi.py
import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
from channels.auth import AuthMiddlewareStack
from klub_chat.consumers import ChatConsumer, MeetingAlertConsumer

# 환경 변수 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # HTTP 요청 처리
    "websocket": AuthMiddlewareStack(
        URLRouter(
            [
                path('ws/chat/<room_name>/', ChatConsumer.as_asgi()),  # 채팅 WebSocket 경로
                path('ws/meeting-alerts/', MeetingAlertConsumer.as_asgi())  # 미팅 알람 WebSocket 경로
            ]
        )
    ),  # WebSocket 요청 처리
})
