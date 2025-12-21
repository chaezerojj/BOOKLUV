from django.shortcuts import render, redirect, get_object_or_404
from .models import Room
from django.utils.text import slugify
from rest_framework.decorators import api_view
from asgiref.sync import sync_to_async
import json
import redis.asyncio as redis
from django.utils import timezone
from django.http import JsonResponse
from klub_talk.models import Meeting

# Redis 설정
REDIS_HOST = "redis"
REDIS_PORT = 6379
REDIS_DB = 0

@api_view(["GET", "POST"])
def room_list(request):
    if request.method == "POST":
        room_name = request.POST.get("room_name")
        if room_name and not Room.objects.filter(name=room_name).exists():
            slug = slugify(room_name)
            Room.objects.create(name=room_name, slug=slug)
        return redirect('chat:room-list')

    rooms = Room.objects.select_related('meeting').all()
    return render(request, 'chat/room_list.html', {'rooms': rooms})

# 비동기적으로 Room 객체 가져오기
@sync_to_async
def get_room_or_404(slug):
    return get_object_or_404(Room, slug=slug)
# 예시로 미팅이 시작될 때 알림을 보낸다면:
from .utils import send_meeting_alert

async def room_detail(request, room_name):
    room = await get_room_or_404(room_name)
    nickname = request.GET.get("nickname", "익명")

    # Meeting 객체 가져오기
    meeting = await sync_to_async(lambda: getattr(room, 'meeting', None))()

    # 현재 시간 로컬 시간으로 변환
    now = timezone.localtime()

    can_chat = False

    # 회의가 있고, 현재 시간이 회의 시작 시간 이후라면 채팅 가능
    if meeting and now >= timezone.localtime(meeting.started_at):
        can_chat = True
        
        # 미팅이 시작되었으면 알림을 보내기
        send_meeting_alert(meeting.title, meeting.started_at)

    # Redis 메시지 가져오기
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    messages_raw = await r.lrange(f'chat_{room.slug}', 0, -1)
    messages = [json.loads(m.decode('utf-8')) for m in messages_raw]
    
    return await sync_to_async(render)(request, "chat/room_detail.html", {
        "room": room,
        "nickname": nickname,
        "messages": messages,
        "can_chat": can_chat
    })



# 오늘 회의 전체 API
def today_meetings(request):
    now = timezone.localtime()
    
    # 오늘 시작 시간과 끝 시간을 설정
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)

    # 오늘의 회의들 조회
    meetings = Meeting.objects.filter(started_at__range=(today_start, today_end))

    data = [
        {
            "title": m.title,
            "started_at": m.started_at.strftime("%H:%M"),
            "room_slug": m.room.slug if hasattr(m, 'room') and m.room else ""
        }
        for m in meetings
    ]
    return JsonResponse({"meetings": data})
