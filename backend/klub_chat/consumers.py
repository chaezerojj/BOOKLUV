import json
import redis.asyncio as redis

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone

from .models import Room
from klub_talk.models import Participate

REDIS_HOST = "redis"
REDIS_PORT = 6379
REDIS_DB = 0


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            await self.close()
            return

        self.room = await self.get_room()
        self.redis = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
        )

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        await self.add_online_user()
        await self.broadcast_participants_status()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "system_message",
                "message": f"{self.user.nickname}님이 입장하셨습니다."
            }
        )

    async def disconnect(self, close_code):
        await self.remove_online_user()
        await self.broadcast_participants_status()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "system_message",
                "message": f"{self.user.nickname}님이 퇴장하셨습니다."
            }
        )

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # =====================
    # 메시지 수신
    # =====================
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message")

        if not await self.is_meeting_active():
            await self.send(text_data=json.dumps({
                "type": "error",
                "message": "회의 시간이 아닙니다."
            }))
            return

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": self.user.nickname,
                "timestamp": timezone.localtime().isoformat(),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "chat",
            "message": event["message"],
            "username": event["username"],
            "timestamp": event["timestamp"],
        }))

    async def system_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "system",
            "message": event["message"],
            "timestamp": timezone.localtime().isoformat(),
        }))

    # =====================
    # 참가자 상태
    # =====================
    async def broadcast_participants_status(self):
        participants = await self.get_participants_status()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "participants_status",
                "participants": participants,
            }
        )

    async def participants_status(self, event):
        await self.send(text_data=json.dumps({
            "type": "participants",
            "participants": event["participants"],
        }))

    async def add_online_user(self):
        key = f"chat_room_users_{self.room.slug}"
        await self.redis.sadd(key, self.user.id)

    async def remove_online_user(self):
        key = f"chat_room_users_{self.room.slug}"
        await self.redis.srem(key, self.user.id)

    async def get_participants_status(self):
        meeting = await self.get_meeting()
        if not meeting:
            return []

        users = await self.get_confirmed_users(meeting)

        key = f"chat_room_users_{self.room.slug}"
        online_ids = set(map(int, await self.redis.smembers(key)))

        return [
            {
                "id": user.id,
                "username": user.nickname,
                "online": user.id in online_ids,
            }
            for user in users
        ]

    # =====================
    # DB helpers
    # =====================
    @database_sync_to_async
    def get_room(self):
        return Room.objects.select_related("meeting").get(slug=self.room_name)

    @database_sync_to_async
    def get_meeting(self):
        return getattr(self.room, "meeting", None)

    @database_sync_to_async
    def is_meeting_active(self):
        meeting = getattr(self.room, "meeting", None)
        if not meeting:
            return False

        now = timezone.localtime()
        start = timezone.localtime(meeting.started_at)
        end = timezone.localtime(meeting.finished_at)

        return start <= now <= end

    @database_sync_to_async
    def get_confirmed_users(self, meeting):
        users = [meeting.leader_id]

        participants = Participate.objects.filter(
            meeting=meeting,
            result=True
        ).select_related("user_id")

        users.extend(p.user_id for p in participants)

        return list({u.id: u for u in users}.values())


# =========================
# 🔔 미팅 알림 Consumer
# =========================
class MeetingAlertConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "meeting_alerts"

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
        print("🔥 send_meeting_alert called:", event)  # <- 확인용
        await self.send(text_data=json.dumps({
            "title": event["title"],
            "started_at": event["started_at"],  # 이미 KST
            "meeting_id": event["meeting_id"],
            "join_url": event.get("join_url", "#"),
        }))
