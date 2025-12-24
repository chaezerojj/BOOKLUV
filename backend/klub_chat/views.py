import json
import redis
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Q
from django.db import transaction
from .models import Room
from klub_talk.models import Meeting, Participate

# =====================
# Redis 설정
# =====================
REDIS_HOST = "redis"
REDIS_PORT = 6379
REDIS_DB = 0


# =====================
# 채팅방 목록
# =====================

@login_required
def room_list(request):
    user = request.user
    now = timezone.localtime()

    # 1. 오늘 날짜 범위 설정 (00:00:00 ~ 23:59:59)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)

    # 2. 오늘 미팅 중 방(room)이 없는 미팅들만 조회
    # (이미 방이 있는 미팅은 제외하여 중복 생성 방지)
    meetings_to_create_room = Meeting.objects.filter(
        started_at__range=(today_start, today_end),
        room__isnull=True
    )

    # 3. 데이터베이스 트랜잭션을 사용하여 방 일괄 생성
    if meetings_to_create_room.exists():
        with transaction.atomic():
            for meeting in meetings_to_create_room:
                Room.objects.create(
                    name=meeting.title,
                    slug=f"{slugify(meeting.title)}-{meeting.id}", # 제목-ID 형태
                    meeting=meeting  # 미팅과 외래키 연결
                )

    # 현재 유저가 참여 확정된 미팅 ID들
    participated_meetings = Participate.objects.filter(
        user_id=user, result=True
    ).values_list("meeting", flat=True)

    # 내가 리더이거나 참여자인 '오늘'의 방들만 필터링해서 보여주기
    rooms = Room.objects.filter(
        Q(meeting_id__in=participated_meetings) | Q(meeting__leader_id=user)
    ).filter(
        meeting__started_at__range=(today_start, today_end)
    ).select_related("meeting")

    return render(request, "chat/room_list.html", {
        "rooms": rooms,
        "user": user,
    })
# =====================
# 채팅방 상세
# =====================

@login_required
def room_detail(request, room_name):
    room = get_object_or_404(Room, slug=room_name)
    meeting = getattr(room, "meeting", None)
    user = request.user

    # 접근 권한 체크
    if meeting:
        is_participant = meeting.participations.filter(user_id=user, result=True).exists()
        is_leader = meeting.leader_id == user
        if not (is_participant or is_leader):
            return HttpResponseForbidden("채팅방에 접근할 권한이 없습니다.")
    else:
        return HttpResponseForbidden("채팅방에 접근할 권한이 없습니다.")

    nickname = user.nickname
    can_chat = False
    now = timezone.localtime()

    leader = meeting.leader_id if meeting else None

    # 참여자 목록
    participants_qs = meeting.participations.filter(result=True).select_related("user_id") if meeting else []
    
    # 참여자 데이터를 JS에서 id 기준으로 사용
    participants_list = []
    for p in participants_qs:
        participants_list.append({
            "id": p.user_id.id,
            "nickname": p.user_id.nickname,
            "online": False  # 초기값, WebSocket에서 업데이트
        })

    # 리더도 participants_list에 포함
    if leader:
        # 중복 방지
        if not any(p["id"] == leader.id for p in participants_list):
            participants_list.insert(0, {
                "id": leader.id,
                "nickname": leader.nickname,
                "online": False
            })

    total_members = len(participants_list)
    joined_members = len(participants_qs)  # 리더 제외

    # 채팅 가능 여부
    if meeting:
        start = timezone.localtime(meeting.started_at)
        end = timezone.localtime(meeting.finished_at)
        if start <= now <= end:
            can_chat = True

    # Redis 메시지 로드
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
    messages_raw = r.lrange(f"chat_{room.slug}", 0, -1)
    messages = []
    for m in messages_raw:
        msg = json.loads(m)
        msg["user_id"] = msg.get("user_id")  # 저장 시 user_id를 포함해야 함
        if "timestamp" in msg:
            msg["timestamp"] = timezone.localtime(
                timezone.datetime.fromisoformat(msg["timestamp"])
            ).strftime("%Y-%m-%d %H:%M:%S")
        messages.append(msg)

    return render(request, "chat/room_detail.html", {
        "room": room,
        "nickname": nickname,
        "messages": messages,
        "can_chat": can_chat,
        "leader": leader,
        "participants": participants_list,
        "total_members": total_members,
        "joined_members": joined_members,
    })

# =====================
# 오늘의 미팅 (알림/목록용)
# =====================
from datetime import timedelta

@login_required
def today_meetings(request):
    user = request.user
    now = timezone.localtime()
    
    # 1. 필터링 기준 시간 설정
    # 시작 10분 전 미팅들을 포함하기 위해 미래 시간 설정
    ten_minutes_later = now + timedelta(minutes=10)
    
    # 2. 미팅 조건:
    # - 시작 시간(started_at)이 지금으로부터 10분 후보다 이전일 것 (시작 10분 전 진입)
    # - 종료 시간(finished_at)이 아직 지나지 않았을 것 (진행 중인 미팅 포함)
    meetings_today = Meeting.objects.filter(
        started_at__lte=ten_minutes_later,
        finished_at__gte=now
    ).select_related("room")

    # 3. 참여자 혹은 리더 필터링 (기존 로직 유지)
    filtered_meetings = []
    for m in meetings_today:
        is_leader = m.leader_id == user
        is_participant = m.participations.filter(user_id=user, result=True).exists()
        if is_leader or is_participant:
            filtered_meetings.append(m)

    # 4. JSON 응답 구성
    data = []
    for m in filtered_meetings:
        start_local = timezone.localtime(m.started_at)
        # 방이 있을 경우에만 올바른 URL 반환
        join_url = f"/api/v1/chat/rooms/{m.room.slug}/" if hasattr(m, "room") and m.room else "#"
        
        data.append({
            "meeting_id": m.id,
            "title": m.title,
            "started_at": start_local.strftime("%H:%M"),
            "join_url": join_url,
        })

    return JsonResponse({"meetings": data})