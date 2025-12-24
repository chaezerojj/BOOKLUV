import json
import redis
import os
from datetime import timedelta
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from django.db import transaction

from .models import Room
from klub_talk.models import Meeting, Participate

# =====================
# Redis 설정 (Railway URL 반영)
# =====================
# 환경 변수 REDIS_URL이 있으면 그것을 쓰고, 없으면 보내주신 주소를 기본값으로 사용합니다.
REDIS_URL = os.getenv('REDIS_URL', 'redis://default:bGBSgqYKpfUrphgGUScwxHlFkdvRIKYh@redis.railway.internal:6379')

# =====================
# 채팅방 목록 (자동 생성 및 필터링)
# =====================

@login_required
def room_list(request):
    user = request.user
    now = timezone.localtime()

    # 1. 미팅 기준 설정: 시작 10분 전 ~ 아직 종료되지 않은 미팅
    ten_minutes_later = now + timedelta(minutes=10)

    # 2. 방(room)이 없는 조건에 맞는 미팅들 자동 생성
    meetings_to_create_room = Meeting.objects.filter(
        started_at__lte=ten_minutes_later,
        finished_at__gte=now,
        room__isnull=True
    )

    if meetings_to_create_room.exists():
        with transaction.atomic():
            for meeting in meetings_to_create_room:
                Room.objects.create(
                    name=meeting.title,
                    slug=f"{slugify(meeting.title)}-{meeting.id}",
                    meeting=meeting
                )

    # 3. 현재 유저가 참여 확정(result=True)된 미팅 ID 목록
    participated_meetings = Participate.objects.filter(
        user_id=user, result=True
    ).values_list("meeting", flat=True)

    # 4. 필터링: (참여자 OR 리더) AND (시작 10분 전 ~ 종료 전)
    rooms = Room.objects.filter(
        Q(meeting_id__in=participated_meetings) | Q(meeting__leader_id=user)
    ).filter(
        meeting__started_at__lte=ten_minutes_later,
        meeting__finished_at__gte=now
    ).select_related("meeting")

    return render(request, "chat/room_list.html", {
        "rooms": rooms,
        "user": user,
    })

# =====================
# 채팅방 상세 (Redis 인증 에러 해결)
# =====================

@login_required
def room_detail(request, room_name):
    room = get_object_or_404(Room, slug=room_name)
    meeting = getattr(room, "meeting", None)
    user = request.user

    # 접근 권한 체크
    if not meeting:
        return HttpResponseForbidden("연결된 미팅 정보가 없습니다.")

    is_participant = meeting.participations.filter(user_id=user, result=True).exists()
    is_leader = meeting.leader_id == user
    if not (is_participant or is_leader):
        return HttpResponseForbidden("채팅방에 접근할 권한이 없습니다.")

    # 참여자 목록 구성
    participants_qs = meeting.participations.filter(result=True).select_related("user_id")
    participants_list = []
    for p in participants_qs:
        participants_list.append({
            "id": p.user_id.id,
            "nickname": p.user_id.nickname,
            "online": False
        })

    if meeting.leader_id and not any(p["id"] == meeting.leader_id.id for p in participants_list):
        participants_list.insert(0, {
            "id": meeting.leader_id.id,
            "nickname": meeting.leader_id.nickname,
            "online": False
        })

    # 채팅 가능 여부 (현재 시간 기준)
    now = timezone.localtime()
    can_chat = meeting.started_at <= now <= meeting.finished_at

    # 🔥 Redis 메시지 로드 (인증 정보 포함된 URL 사용)
    try:
        r = redis.from_url(REDIS_URL, decode_responses=True)
        messages_raw = r.lrange(f"chat_{room.slug}", 0, -1)
    except Exception as e:
        print(f"Redis 연결 실패: {e}")
        messages_raw = []

    messages = []
    for m in messages_raw:
        msg = json.loads(m)
        if "timestamp" in msg:
            msg["timestamp"] = timezone.localtime(
                timezone.datetime.fromisoformat(msg["timestamp"])
            ).strftime("%Y-%m-%d %H:%M:%S")
        messages.append(msg)

    return render(request, "chat/room_detail.html", {
        "room": room,
        "nickname": user.nickname,
        "messages": messages,
        "can_chat": can_chat,
        "participants": participants_list,
        "total_members": len(participants_list),
    })

# =====================
# 오늘의 미팅 알람 (10분 전 필터링)
# =====================

@login_required
def today_meetings(request):
    user = request.user
    now = timezone.localtime()
    ten_minutes_later = now + timedelta(minutes=10)
    
    # 시작 10분 전 ~ 아직 종료되지 않은 미팅 조회
    meetings_today = Meeting.objects.filter(
        started_at__lte=ten_minutes_later,
        finished_at__gte=now
    ).select_related("room")

    data = []
    for m in meetings_today:
        is_leader = m.leader_id == user
        is_participant = m.participations.filter(user_id=user, result=True).exists()
        
        if is_leader or is_participant:
            # 방이 아직 자동 생성되지 않았을 경우를 대비해 처리
            join_url = f"/api/v1/chat/rooms/{m.room.slug}/" if hasattr(m, "room") and m.room else "#"
            
            data.append({
                "meeting_id": m.id,
                "title": m.title,
                "started_at": timezone.localtime(m.started_at).strftime("%H:%M"),
                "join_url": join_url,
            })

    return JsonResponse({"meetings": data})