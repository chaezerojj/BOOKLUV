import json
import os
import redis.asyncio as redis

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone

from .models import Room
from klub_talk.models import Participate

# =====================
# Redis 설정 (Railway 환경변수 로드)
# =====================
# 제공해주신 내부 URL 주소를 기본값으로 설정합니다.
REDIS_URL = os.getenv('REDIS_URL', 'redis://default:bGBSgqYKpfUrphgGUScwxHlFkdvRIKYh@redis.railway.internal:6379')

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            class MockUser:
                id = 9999
                nickname = f"Tester_{self.channel_name[-5:]}"
                is_authenticated = True
            self.user = MockUser()
            # await self.close()
            return

        # 1. 방 정보 가져오기
        try:
            self.room = await self.get_room()
        except Exception:
            # 방 번호가 -1이거나 존재하지 않는 슬러그일 경우 대비
            await self.close()
            return

        # 2. Redis 연결 (🔥 Authentication required 에러 해결 핵심)
        # redis.Redis(...) 대신 redis.from_url(...)을 사용해야 인증 정보가 적용됩니다.
        self.redis = redis.from_url(REDIS_URL, decode_responses=True)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # 온라인 상태 처리
        await self.add_online_user()
        await self.broadcast_participants_status()

        # 입장 시스템 메시지
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "system_message",
                "message": f"{self.user.nickname}님이 입장하셨습니다."
            }
        )

    async def disconnect(self, close_code):
        # Redis 객체가 생성된 경우에만 실행
        if hasattr(self, 'redis'):
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
        # Redis 연결 닫기
        if hasattr(self, 'redis'):
            await self.redis.close()

    # =====================
    # 메시지 수신 및 발송
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
                "user_id": self.user.id
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "chat",
            "message": event["message"],
            "username": event["username"],
            "timestamp": event["timestamp"],
            "user_id": event["user_id"],
        }))

    async def system_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "system",
            "message": event["message"],
            "timestamp": timezone.localtime().isoformat(),
        }))

    # =====================
    # 참가자 상태 관리
    # =====================
    async def add_online_user(self):
        key = f"chat_room_users_{self.room.slug}"
        await self.redis.sadd(key, self.user.id)

    async def remove_online_user(self):
        key = f"chat_room_users_{self.room.slug}"
        await self.redis.srem(key, self.user.id)

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

    async def get_participants_status(self):
        meeting = await self.get_meeting()
        if not meeting:
            return []

        users = await self.get_confirmed_users(meeting)
        key = f"chat_room_users_{self.room.slug}"

        # Redis에서 온라인 유저 ID 셋 가져오기
        online_members = await self.redis.smembers(key)
        online_ids = {int(uid) for uid in online_members}

        return [
            {
                "id": user.id,
                "nickname": user.nickname, # HTML JS와 이름 맞춤
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
        return meeting.started_at <= now <= meeting.finished_at
    
    @database_sync_to_async
    def get_confirmed_users(self, meeting):
        # 1. 딕셔너리를 사용하여 ID를 키로 저장 (중복 자동 제거)
        users_dict = {}

        # 2. 리더 추가
        if meeting.leader_id:
            users_dict[meeting.leader_id.id] = meeting.leader_id

        # 3. 참여 확정자(result=True)들만 가져오기
        participants = Participate.objects.filter(
            meeting=meeting,
            result=True
        ).select_related("user_id")

        # 4. 참여자 추가 (이미 리더가 포함되어 있다면 덮어쓰기되어 중복 안 됨)
        for p in participants:
            users_dict[p.user_id.id] = p.user_id

        # 5. 최종 리스트 반환
        return list(users_dict.values())

# =========================
# 🔔 미팅 알림 Consumer
# =========================
class MeetingAlertConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "meeting_alerts"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_meeting_alert(self, event):
        await self.send(text_data=json.dumps({
            "title": event["title"],
            "started_at": event["started_at"],
            "meeting_id": event["meeting_id"],
            "join_url": event.get("join_url", "#"),
        }))