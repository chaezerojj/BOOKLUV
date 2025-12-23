import json
import redis

from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse

from .models import Room
from klub_talk.models import Meeting

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
    if request.method == "POST":
        room_name = request.POST.get("room_name")

        if room_name and not Room.objects.filter(name=room_name).exists():
            Room.objects.create(
                name=room_name,
                slug=slugify(room_name)
            )

        return redirect("chat:room-list")

    rooms = Room.objects.select_related("meeting").all()

    return render(request, "chat/room_list.html", {
        "rooms": rooms,
        "user": request.user,
    })


# =====================
# 채팅방 상세
# =====================
@login_required
def room_detail(request, room_name):
    room = get_object_or_404(Room, slug=room_name)
    meeting = getattr(room, "meeting", None)

    nickname = request.user.nickname

    can_chat = False
    leader = None
    participants = []

    total_members = 0
    joined_members = 0

    now = timezone.localtime()

    if meeting:
        start = timezone.localtime(meeting.started_at)
        end = timezone.localtime(meeting.finished_at)

        if start <= now <= end:
            can_chat = True

        leader = meeting.leader_id

        participants = (
            meeting.participations
            .filter(result=True)
            .select_related("user_id")
        )

        joined_members = participants.count()
        total_members = joined_members + 1  # 리더 포함

    r = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        decode_responses=True,
    )

    messages_raw = r.lrange(f"chat_{room.slug}", 0, -1)
    messages = []
    
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(start, end)
    
    for m in messages_raw:
        msg = json.loads(m)
        # 🔥 timestamp가 있으면 KST 변환
        if "timestamp" in msg:
            msg["timestamp"] = timezone.localtime(
                timezone.datetime.fromisoformat(msg["timestamp"])
            ).strftime("%Y-%m-%d %H:%M:%S")
        messages.append(msg)


    return render(
        request,
        "chat/room_detail.html",
        {
            "room": room,
            "nickname": nickname,
            "messages": messages,
            "can_chat": can_chat,
            "leader": leader,
            "participants": participants,
            "total_members": total_members,
            "joined_members": joined_members,
        }
    )


# =====================
# 오늘의 미팅 (알림/목록용)
# =====================
@login_required
def today_meetings(request):
    now = timezone.localtime()

    today_start_local = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end_local = now.replace(hour=23, minute=59, second=59, microsecond=999999)

    # 🔥 UTC 기준으로 변환해서 조회
    today_start_utc = timezone.make_aware(
        today_start_local.replace(tzinfo=None),
        timezone.get_current_timezone()
    ).astimezone(timezone.utc)

    today_end_utc = timezone.make_aware(
        today_end_local.replace(tzinfo=None),
        timezone.get_current_timezone()
    ).astimezone(timezone.utc)

    meetings = Meeting.objects.filter(
        started_at__range=(today_start_utc, today_end_utc)
    ).select_related("room")

    data = []

    for m in meetings:
        start_local = timezone.localtime(m.started_at)

        join_url = (
            f"/api/v1/chat/rooms/{m.room.slug}/"
            if hasattr(m, "room") and m.room
            else "#"
        )

        data.append({
            "title": m.title,
            "started_at": start_local.strftime("%H:%M"),
            "join_url": join_url,
        })

    return JsonResponse({"meetings": data})