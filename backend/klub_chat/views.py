# klub_chat/views.py
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
from .utils import send_meeting_alert

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

@sync_to_async
def get_room_or_404(slug):
    return get_object_or_404(Room, slug=slug)

async def room_detail(request, room_name):
    room = await get_room_or_404(room_name)
    nickname = request.GET.get("nickname", "익명")
    meeting = await sync_to_async(lambda: getattr(room, 'meeting', None))()
    now = timezone.localtime()
    can_chat = False

    if meeting:
        if now >= timezone.localtime(meeting.started_at) and now <= timezone.localtime(meeting.finished_at):
            can_chat = True
        if can_chat:
            # 회의 참여 링크 포함
            join_url = f"/rooms/{room.slug}/?nickname={nickname}" if room.slug else "#"
            await send_meeting_alert(meeting.title, meeting.started_at, meeting.id, join_url)

    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    messages_raw = await r.lrange(f'chat_{room.slug}', 0, -1)
    messages = [json.loads(m.decode('utf-8')) for m in messages_raw]

    return await sync_to_async(render)(request, "chat/room_detail.html", {
        "room": room,
        "nickname": nickname,
        "messages": messages,
        "can_chat": can_chat
    })

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
