from django.shortcuts import render, redirect, get_object_or_404
from .models import Room
from django.utils.text import slugify
from rest_framework.decorators import api_view
from asgiref.sync import sync_to_async
import json
import redis.asyncio as redis

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

    rooms = Room.objects.all()
    return render(request, 'chat/room_list.html', {'rooms': rooms})

@sync_to_async
def get_room_or_404(slug):
    return get_object_or_404(Room, slug=slug)

async def room_detail(request, room_name):
    room = await get_room_or_404(room_name)
    nickname = request.GET.get("nickname", "익명")

    # Redis 연결
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    messages_raw = await r.lrange(f'chat_{room.slug}', 0, -1)
    messages = [json.loads(m.decode('utf-8')) for m in messages_raw]

    return await sync_to_async(render)(request, "chat/room_detail.html", {
        "room": room,
        "nickname": nickname,
        "messages": messages
    })
