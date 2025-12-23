# klub_chat/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Room
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from asgiref.sync import sync_to_async
import json
import redis.asyncio as redis
from django.utils import timezone
from django.http import JsonResponse, HttpResponseRedirect
from klub_talk.models import Meeting
from .utils import send_meeting_alert

REDIS_HOST = "redis"
REDIS_PORT = 6379
REDIS_DB = 0

@sync_to_async
def is_authenticated(request):
    return request.user.is_authenticated

@login_required(login_url='/accounts/login/')
@api_view(["GET", "POST"])
def room_list(request):
    if request.method == "POST":
        room_name = request.POST.get("room_name")
        if room_name and not Room.objects.filter(name=room_name).exists():
            slug = slugify(room_name)
            Room.objects.create(name=room_name, slug=slug)
        return redirect('chat:room-list')
    user = request.user
    rooms = Room.objects.select_related('meeting').all()
    
    context = {
        'rooms' : rooms,
        'user' : user
    }
    return render(request, 'chat/room_list.html',context)

@sync_to_async
def get_room_or_404(slug):
    return get_object_or_404(Room, slug=slug)

# klub_chat/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Room
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from asgiref.sync import sync_to_async
import json
import redis.asyncio as redis
from django.utils import timezone
from django.http import JsonResponse, HttpResponseRedirect
from klub_talk.models import Meeting
from .utils import send_meeting_alert

REDIS_HOST = "redis"
REDIS_PORT = 6379
REDIS_DB = 0

@sync_to_async
def is_authenticated(request):
    return request.user.is_authenticated

@api_view(["GET", "POST"])
@login_required(login_url="/accounts/login/")
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
        "user": request.user,  # 템플릿에서 {{ user.nickname }}
    })

@sync_to_async
def get_room_or_404(slug):
    return get_object_or_404(Room, slug=slug)


@sync_to_async
def is_authenticated(user):
    return user.is_authenticated


@sync_to_async
def get_user_nickname(user):
    return getattr(user, "nickname", user.nickname)

async def room_detail(request, room_name):
    # ✅ 로그인 체크
    if not await is_authenticated(request.user):
        return HttpResponseRedirect(
            f"/accounts/login/?next={request.path}"
        )

    room = await get_room_or_404(room_name)
    nickname = await get_user_nickname(request.user)

    meeting = await sync_to_async(lambda: getattr(room, "meeting", None))()
    now = timezone.localtime()
    can_chat = False

    if meeting:
        started_at = meeting.started_at
        finished_at = meeting.finished_at

        if started_at <= now <= finished_at:
            can_chat = True

            # 🔔 미팅 시작 알림 (한 번만 보내게 utils에서 제어 권장)
            join_url = f"/api/v1/chat/rooms/{room.slug}/"
            await send_meeting_alert(
                meeting.title,
                meeting.started_at,
                meeting.id,
                join_url
            )

    # 📦 Redis 메시지 로드
    r = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB
    )

    messages_raw = await r.lrange(f"chat_{room.slug}", 0, -1)
    messages = [json.loads(m.decode("utf-8")) for m in messages_raw]

    return await sync_to_async(render)(
        request,
        "chat/room_detail.html",
        {
            "room": room,
            "nickname": nickname,
            "user": request.user,
            "messages": messages,
            "can_chat": can_chat,
        }
    )

def today_meetings(request):
    now = timezone.localtime()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    meetings = Meeting.objects.filter(started_at__range=(today_start, today_end))

    data = []
    for m in meetings:
        if hasattr(m, 'room') and m.room:
            join_url = f"/rooms/{m.room.slug}/?nickname=익명"
        else:
            join_url = "#"
        data.append({
            "title": m.title,
            "started_at": m.started_at.strftime("%H:%M"),
            "join_url": join_url
        })

    return JsonResponse({"meetings": data})

@login_required(login_url="/accounts/login/")
def today_meetings(request):
    now = timezone.localtime()

    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)

    meetings = Meeting.objects.filter(
        started_at__range=(today_start, today_end)
    )

    data = []

    for m in meetings:
        if hasattr(m, "room") and m.room:
            join_url = f"/api/v1/chat/rooms/{m.room.slug}/"
        else:
            join_url = "#"

        data.append({
            "title": m.title,
            "started_at": m.started_at.strftime("%H:%M"),
            "join_url": join_url,
        })

    return JsonResponse({"meetings": data})
