from klub_chat.models import Room
from klub_talk.models import Meeting
from django.utils import timezone
from celery import shared_task
from django.utils.text import slugify
from django.db import IntegrityError
from datetime import datetime, time
from django.utils.timezone import make_aware

def generate_unique_slug(name):
    """
    이미 존재하는 slug가 있으면 '-1', '-2', ... 붙여서 유니크하게 만듦
    """
    base_slug = slugify(name)
    slug = base_slug
    counter = 1
    while Room.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug

@shared_task
def check_and_create_rooms():
    now = timezone.localtime()
    today_start = make_aware(datetime.combine(now.date(), time.min))
    today_end = make_aware(datetime.combine(now.date(), time.max))

    # 오늘 시작하는 모든 회의
    meetings_today = Meeting.objects.filter(started_at__range=(today_start, today_end))

    for meeting in meetings_today:
        # 이미 Room이 없으면 새로 생성
        if not hasattr(meeting, 'room'):
            try:
                Room.objects.create(
                    name=meeting.title,
                    meeting=meeting,
                    slug=generate_unique_slug(meeting.title)
                )
            except IntegrityError:
                # 혹시 slug 충돌 시 재생성
                Room.objects.create(
                    name=meeting.title,
                    meeting=meeting,
                    slug=generate_unique_slug(meeting.title)
                )

    # 기존 Room 중 slug가 없는 경우 채우기
    rooms_without_slug = Room.objects.filter(slug="")
    for room in rooms_without_slug:
        room.slug = generate_unique_slug(room.name)
        room.save()
