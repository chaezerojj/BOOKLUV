from django.shortcuts import render, redirect
from .models import Room
from django.utils.text import slugify
from django.http import Http404

def room_list(request):
    if request.method == "POST":
        room_name = request.POST.get("room_name")
        if room_name and not Room.objects.filter(name=room_name).exists():
            # 방 이름과 슬러그 저장
            slug = slugify(room_name)
            Room.objects.create(name=room_name, slug=slug)
        return redirect('chat:room_list')  # POST 후 리다이렉트

    rooms = Room.objects.all()
    return render(request, 'chat/room_list.html', {'rooms': rooms})

from django.shortcuts import get_object_or_404, redirect, render
from .models import Room

from asgiref.sync import sync_to_async
import json
import redis.asyncio as redis
from django.shortcuts import render
from .models import Room

REDIS_URL = "redis://localhost:6379/0"

@sync_to_async
def get_room(room_name):
    return Room.objects.get(slug=room_name)

async def room_detail(request, room_name):
    room = await get_room(room_name)
    nickname = request.GET.get('nickname', '익명')
    
    r = await redis.from_url(REDIS_URL)
    messages_raw = await r.lrange(f'chat_{room.slug}', 0, -1)
    messages = [json.loads(m.decode('utf-8')) for m in messages_raw]

    return render(request, "chat/room_detail.html", {
        "room": room,
        "nickname": nickname,
        "messages": messages
    })