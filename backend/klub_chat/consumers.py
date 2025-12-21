# klub_chat/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # 방 그룹에 조인
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # 방 그룹에서 나가기
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # 방 그룹에서 메시지를 수신했을 때 처리
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        nickname = text_data_json['nickname']

        # 방 그룹으로 메시지 전송
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'nickname': nickname
            }
        )

    # 채팅 메시지를 웹소켓으로 전송
    async def chat_message(self, event):
        message = event['message']
        nickname = event['nickname']

        # 웹소켓으로 메시지 전송
        await self.send(text_data=json.dumps({
            'message': message,
            'nickname': nickname
        }))

class MeetingAlertConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # 미팅 알람 구독 (여러 미팅이 있으면 구독할 방을 구분할 수 있도록 추가 가능)
        self.group_name = 'meeting_alerts'
        
        # 알림 그룹에 조인
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # 알림 그룹에서 나가기
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # 미팅 알람 메시지를 받을 때
    async def receive(self, text_data):
        pass  # 미팅 알람 메시지는 서버에서 발송되므로, 클라이언트에서 직접 메시지를 받을 필요는 없습니다.

    # 미팅 알림을 웹소켓으로 전송
    async def send_meeting_alert(self, event):
        # 'event'는 미팅 알림 정보
        title = event['title']
        started_at = event['started_at']

        # 웹소켓으로 미팅 알림 전송
        await self.send(text_data=json.dumps({
            'title': title,
            'started_at': started_at
        }))
