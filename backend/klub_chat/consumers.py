import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone  # 타임존을 처리하기 위한 임포트
from .models import Room, Meeting


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # 방 정보 가져오기 (비동기적으로 처리)
        self.room = await self.get_room()

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        nickname = data.get('nickname')

        # 회의 중이 아니면 차단
        if not await self.is_meeting_active(self.room):
            await self.send(text_data=json.dumps({
                'error': '회의 시간이 아닙니다. 채팅이 불가능합니다.'
            }))
            return

        # 회의 중일 때만 메시지 전송
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'nickname': nickname
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'nickname': event['nickname']
        }))

    # 비동기적으로 Room 객체 가져오기
    @database_sync_to_async
    def get_room(self):
        return Room.objects.get(slug=self.room_name)

    # 비동기적으로 회의 상태 확인
    @database_sync_to_async
    def is_meeting_active(self, room):
        """회의가 진행 중인지 확인하는 함수"""
        meeting = getattr(room, 'meeting', None)
        if not meeting:
            return False
        now = timezone.now()
        return meeting.started_at <= now <= meeting.finished_at


class MeetingAlertConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'meeting_alerts'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_meeting_alert(self, event):
        await self.send(text_data=json.dumps({
            'title': event['title'],
            'started_at': event['started_at']
        }))
