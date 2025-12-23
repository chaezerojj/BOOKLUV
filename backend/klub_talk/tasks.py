# klub_chat/tasks.py
from celery import shared_task
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db import IntegrityError
from django.utils.text import slugify
from datetime import datetime, time

@shared_task
def check_and_create_rooms():
    """
    오늘 시작하는 회의를 기반으로 Room 생성 및 slug 채우기
    """
    from klub_chat.models import Room
    from klub_talk.models import Meeting

    def generate_unique_slug(name):
        base_slug = slugify(name) or "room"
        slug = base_slug
        counter = 1
        while Room.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    now = timezone.localtime()
    today_start = datetime.combine(now.date(), time.min)
    today_end = datetime.combine(now.date(), time.max)

    meetings_today = Meeting.objects.filter(started_at__range=(today_start, today_end))

    for meeting in meetings_today:
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


@shared_task
def send_today_meeting_alarms(meeting_id):
    """
    특정 회의 시작 10분 전 알람 전송 (WebSocket + DB 기록)
    """
    from klub_talk.models import Meeting
    from klub_chat.models import MeetingAlert

    try:
        meeting = Meeting.objects.get(id=meeting_id)
    except Meeting.DoesNotExist:
        return

    # 이미 알람이 존재하는지 체크
    if not MeetingAlert.objects.filter(meeting=meeting).exists():
        # user 필드에 leader_id 사용
        MeetingAlert.objects.create(meeting=meeting, user=meeting.leader_id)

    # WebSocket 알람
    channel_layer = get_channel_layer()

    # 회의 참여 링크 생성
    room_slug = meeting.room.slug if hasattr(meeting, 'room') and meeting.room else ""
    join_url = f"/api/v1/chat/rooms/{room_slug}/?nickname=익명" if room_slug else "#"

    async_to_sync(channel_layer.group_send)(
        "meeting_alerts",
        {
            "type": "send_meeting_alert",
            "title": meeting.title,
            "started_at": timezone.localtime(meeting.started_at).strftime('%Y-%m-%d %H:%M:%S'),
            "meeting_id": meeting.id,
            "join_url": join_url,   # 링크 포함
        }
    )

@shared_task
def send_today_meeting_alarms_for_today():
    """
    오늘의 모든 회의에 대해 시작 10분 전 알람 전송
    """
    from klub_talk.models import Meeting
    from datetime import datetime, time
    from django.utils import timezone
    from .tasks import send_today_meeting_alarms  # 개별 회의용 태스크

    now = timezone.localtime()
    today_start = datetime.combine(now.date(), time.min)
    today_end = datetime.combine(now.date(), time.max)
    
    meetings_today = Meeting.objects.filter(started_at__range=(today_start, today_end))

    for meeting in meetings_today:
        send_today_meeting_alarms.delay(meeting.id)