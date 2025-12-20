import json
from channels.generic.websocket import AsyncWebsocketConsumer

class AlarmConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # 로그인한 유저별로 그룹을 생성합니다 (user_1, user_2 등)
        if self.scope["user"].is_authenticated:
            self.group_name = f"user_{self.scope['user'].id}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # 🔹 백엔드에서 호출할 메서드
    async def alarm_message(self, event):
        await self.send(text_data=json.dumps(event["content"]))