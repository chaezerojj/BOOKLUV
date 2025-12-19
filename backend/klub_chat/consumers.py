# klub_chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, ChatMessage
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        nickname = data['nickname']
        message = data['message']

        # DB에 저장 (Async-safe)
        await self.save_message(self.room_name, nickname, message)

        # 그룹에 브로드캐스트
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'nickname': nickname,
                'message': message
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'nickname': event['nickname'],
            'message': event['message']
        }))

    @database_sync_to_async
    def save_message(self, room_name, nickname, message):
        room = Room.objects.get(slug=room_name)
        ChatMessage.objects.create(room=room, nickname=nickname, message=message)
