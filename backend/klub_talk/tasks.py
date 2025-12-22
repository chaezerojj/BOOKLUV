# klub_chat/tasks.py
from klub_chat.models import Room
from klub_talk.models import Meeting
from django.utils import timezone
from celery import shared_task
from django.utils.text import slugify
from django.db import IntegrityError
from datetime import datetime, time, timedelta
from django.utils.timezone import make_aware
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
# klub_talk/signals.py


def generate_unique_slug(name):
    base_slug = slugify(name) or "room"  # name이 비었을 때 대비
    slug = base_slug
    counter = 1
    while Room.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug


@shared_task
def check_and_create_rooms():
    """
    오늘 시작하는 회의 기반으로 Room 생성 및 슬러그 채우기
    """
    now = timezone.localtime()
    today_start = make_aware(datetime.combine(now.date(), time.min))
    today_end = make_aware(datetime.combine(now.date(), time.max))

    meetings_today = Meeting.objects.filter(started_at__range=(today_start, today_end))

    for meeting in meetings_today:
        # 이미 Room이 없으면 생성
        if not hasattr(meeting, 'room') or not meeting.room:
            try:
                Room.objects.create(
                    name=meeting.title,
                    meeting=meeting,
                    slug=generate_unique_slug(meeting.title)
                )
            except IntegrityError:
                Room.objects.create(
                    name=meeting.title,
                    meeting=meeting,
                    slug=generate_unique_slug(meeting.title)
                )

    # Room 중 slug 없는 경우 채우기
    rooms_without_slug = Room.objects.filter(slug="")
    for room in rooms_without_slug:
        room.slug = generate_unique_slug(room.name)
        room.save()


@shared_task
def send_today_meeting_alarms():
    now = timezone.localtime()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)

    # 오늘 시작되는 미팅 목록을 가져옵니다.
    meetings = Meeting.objects.filter(started_at__range=(today_start, today_end))

    channel_layer = get_channel_layer()

    for meeting in meetings:
        room = getattr(meeting, 'room', None)
        if room and room.slug:
            # 메시지 생성
            message = f"'{meeting.title}' 미팅이 {meeting.started_at.strftime('%H:%M')}에 시작됩니다!"
            
            # WebSocket을 통해 메시지 전송 (meeting_alerts 그룹으로 전송)
            async_to_sync(channel_layer.group_send)(
                "meeting_alerts",  # WebSocket 그룹 이름
                {
                    "type": "send_meeting_alert",  # consumer에서 정의한 메시지 타입
                    "title": meeting.title,
                    "started_at": meeting.started_at.strftime('%Y-%m-%d %H:%M:%S'),  # ISO 형식으로 전송
                }
            )
