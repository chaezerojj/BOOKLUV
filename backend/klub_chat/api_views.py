# klub_chat/api_views.py
import json
import os
import redis
from datetime import timedelta

from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.text import slugify
from django.db.models import Q

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Room
from klub_talk.models import Meeting, Participate

REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://default:bGBSgqYKpfUrphgGUScwxHlFkdvRIKYh@redis.railway.internal:6379"
)


def _safe_nick(user):
    return getattr(user, "nickname", None) or getattr(user, "username", None) or getattr(user, "email", None) or "Unknown"


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def rooms_api(request):
    """
    GET /api/v1/chat/api/rooms/
    - 템플릿 room_list 로직을 그대로 JSON화
    """
    user = request.user
    now = timezone.localtime()
    ten_minutes_later = now + timedelta(minutes=10)

    # 1) 방이 없는 meeting 자동 생성(기존 로직 유지)
    meetings_to_create_room = Meeting.objects.filter(
        started_at__lte=ten_minutes_later,
        finished_at__gte=now,
        room__isnull=True,
    )

    if meetings_to_create_room.exists():
        for meeting in meetings_to_create_room:
            new_slug = f"{slugify(meeting.title)}-{meeting.id}"
            Room.objects.get_or_create(
                meeting=meeting,
                defaults={"name": meeting.title, "slug": new_slug},
            )

    # 2) 현재 유저가 참여 확정된 meeting id들
    participated_meetings = Participate.objects.filter(
        user_id=user, result=True
    ).values_list("meeting", flat=True)

    # 3) (참여자 OR 리더) AND (시작 10분 전 ~ 종료 전)
    rooms = (
        Room.objects.filter(
            Q(meeting_id__in=participated_meetings) | Q(meeting__leader_id=user)
        )
        .filter(meeting__started_at__lte=ten_minutes_later, meeting__finished_at__gte=now)
        .select_related("meeting", "meeting__leader_id")
        .order_by("meeting__started_at")
    )

    data = []
    for r in rooms:
        m = r.meeting
        data.append(
            {
                "slug": r.slug,
                "name": r.name,
                "meeting_id": m.id if m else None,
                "meeting_title": m.title if m else None,
                "started_at": timezone.localtime(m.started_at).isoformat() if m and m.started_at else None,
                "finished_at": timezone.localtime(m.finished_at).isoformat() if m and m.finished_at else None,
                "leader": {
                    "id": m.leader_id.id if m and m.leader_id else None,
                    "nickname": _safe_nick(m.leader_id) if m and m.leader_id else None,
                },
            }
        )

    return Response({"rooms": data})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def room_detail_api(request, room_slug):
    """
    GET /api/v1/chat/api/rooms/<slug>/
    - 템플릿 room_detail 로직을 그대로 JSON화
    - participants 기본 online=False (WS로 들어오면 online 갱신됨)
    - Redis에서 messages 로드(기존 템플릿처럼)
    """
    room = get_object_or_404(Room.objects.select_related("meeting", "meeting__leader_id"), slug=room_slug)
    meeting = getattr(room, "meeting", None)
    user = request.user

    if not meeting:
        return Response({"detail": "연결된 미팅 정보가 없습니다."}, status=400)

    is_participant = meeting.participations.filter(user_id=user, result=True).exists()
    is_leader = meeting.leader_id == user
    if not (is_participant or is_leader):
        return Response({"detail": "채팅방에 접근할 권한이 없습니다."}, status=403)

    # participants (중복 제거: 리더 + 확정참여자)
    participants_dict = {}

    # 확정 참여자
    qs = meeting.participations.filter(result=True).select_related("user_id")
    for p in qs:
        participants_dict[p.user_id.id] = {
            "id": p.user_id.id,
            "nickname": _safe_nick(p.user_id),
            "online": False,
        }

    # 리더
    if meeting.leader_id:
        participants_dict[meeting.leader_id.id] = {
            "id": meeting.leader_id.id,
            "nickname": _safe_nick(meeting.leader_id),
            "online": False,
            "isLeader": True,
        }

    participants = list(participants_dict.values())
    # leader first
    if meeting.leader_id:
        participants.sort(key=lambda x: x.get("id") != meeting.leader_id.id)

    # can_chat
    now = timezone.localtime()
    can_chat = meeting.started_at <= now <= meeting.finished_at

    # Redis messages (템플릿 방식 그대로)
    messages = []
    try:
        r = redis.from_url(REDIS_URL, decode_responses=True)
        raw = r.lrange(f"chat_{room.slug}", 0, -1)
        for m in raw:
            msg = json.loads(m)
            # timestamp가 문자열일 수도 있어 방어
            ts = msg.get("timestamp")
            if ts:
                try:
                    msg["timestamp"] = timezone.localtime(
                        timezone.datetime.fromisoformat(ts)
                    ).isoformat()
                except Exception:
                    pass
            messages.append(msg)
    except Exception:
        messages = []

    payload = {
        "room": {"slug": room.slug, "name": room.name},
        "meeting": {
            "id": meeting.id,
            "title": meeting.title,
            "started_at": timezone.localtime(meeting.started_at).isoformat() if meeting.started_at else None,
            "finished_at": timezone.localtime(meeting.finished_at).isoformat() if meeting.finished_at else None,
        },
        "current_user": {"id": user.id, "nickname": _safe_nick(user)},
        "leader": {"id": meeting.leader_id.id, "nickname": _safe_nick(meeting.leader_id)} if meeting.leader_id else None,
        "can_chat": can_chat,
        "participants": participants,
        "total_members": len(participants),
        "messages": messages,
    }
    return Response(payload)
