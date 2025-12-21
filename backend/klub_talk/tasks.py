from celery import shared_task
from django.utils import timezone
from datetime import timedelta

@shared_task
def check_and_create_rooms():
    from .models import Meeting
    from klub_chat.models import Room

    now = timezone.now()
    ten_minutes_later = now + timedelta(minutes=10)

    meetings = Meeting.objects.filter(started_at__range=(now, ten_minutes_later))
    for meeting in meetings:
        if not Room.objects.filter(meeting=meeting).exists():
            Room.objects.create(meeting=meeting)
            print(f"[{timezone.now()}] Room created for meeting: {meeting.title}")
