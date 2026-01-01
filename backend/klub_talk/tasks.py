# klub_talk/tasks.py
from celery import shared_task
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db import IntegrityError
from django.utils.text import slugify
from datetime import datetime, time, timedelta


from celery import shared_task
from django.utils import timezone
from django.utils.text import slugify

@shared_task
def check_and_create_rooms():
    from klub_talk.models import Meeting
    from klub_chat.models import Room
    from django.utils.text import slugify
    
    target_time = timezone.now() + timedelta(minutes=10)
    pending_meetings = Meeting.objects.filter(
        started_at__lte=target_time,
        room__isnull=True
    )

    results = []
    for meeting in pending_meetings:
        try:
            # ✅ 슬러그에 미팅 ID를 붙여서 절대 중복되지 않게 합니다.
            # 예: "미팅-제목-240"
            unique_slug = f"{slugify(meeting.title) or 'room'}-{meeting.id}"
            
            room, created = Room.objects.get_or_create(
                meeting=meeting,
                defaults={
                    'name': meeting.title,
                    'slug': unique_slug
                }
            )
            if created:
                msg = f"✅ 방 생성 성공: {meeting.title} (ID: {meeting.id})"
            else:
                msg = f"ℹ️ 이미 존재: {meeting.title}"
            print(msg)
            results.append(msg)
        except Exception as e:
            error_msg = f"❌ 생성 실패 ({meeting.id}): {str(e)}"
            print(error_msg)
            results.append(error_msg)
            
    return "\n".join(results) if results else "생성할 방이 없습니다."
# =========================
# 미팅 시작 알람 (웹소켓)
# =========================
@shared_task
def send_today_meeting_alarms(meeting_id):
    from klub_talk.models import Meeting
    from klub_chat.models import MeetingAlert

    try:
        meeting = Meeting.objects.get(id=meeting_id)
    except Meeting.DoesNotExist:
        return

    # Create MeetingAlert records for leader and confirmed participants
    users_to_alert = set()
    if meeting.leader_id:
        users_to_alert.add(meeting.leader_id.id)

    participant_qs = meeting.participations.filter(result=True).select_related('user_id')
    for p in participant_qs:
        if p.user_id:
            users_to_alert.add(p.user_id.id)

    for user_id in users_to_alert:
        try:
            MeetingAlert.objects.get_or_create(meeting=meeting, user_id=user_id)
        except Exception:
            # ignore (e.g., race conditions or integrity errors)
            pass

    channel_layer = get_channel_layer()

    room_slug = meeting.room.slug if meeting.room else ""
    join_url = f"/api/v1/chat/rooms/{room_slug}/?nickname=익명" if room_slug else "#"

    async_to_sync(channel_layer.group_send)(
        "meeting_alerts",
        {
            "type": "send_meeting_alert",
            "title": meeting.title,
            "started_at": timezone.localtime(meeting.started_at).strftime(
                "%Y-%m-%d %H:%M"
            ),
            "meeting_id": meeting.id,
            "join_url": join_url,
        }
    )


# =========================
# 오늘 모든 미팅 알람 트리거
# =========================
@shared_task
def send_today_meeting_alarms_for_today():
    from klub_talk.models import Meeting

    now = timezone.localtime()
    # 10분 뒤
    target_time_start = now + timedelta(minutes=10)
    target_time_end = target_time_start + timedelta(seconds=59)  # 1분 간격

    meetings_upcoming = Meeting.objects.filter(
        started_at__range=(target_time_start, target_time_end)
    )

    for meeting in meetings_upcoming:
        send_today_meeting_alarms.delay(meeting.id)

# =========================
# 채팅방 시스템 메시지 (1분 주기)
# =========================
@shared_task
def send_meeting_system_messages():
    from klub_talk.models import Meeting

    channel_layer = get_channel_layer()
    now = timezone.localtime()

    meetings = Meeting.objects.filter(room__isnull=False).select_related("room")
    for meeting in meetings:
        if not meeting.room:
            continue

        room_group = f"chat_{meeting.room.slug}"

        start_at = timezone.localtime(meeting.started_at)
        end_at = timezone.localtime(meeting.finished_at)

        diff = start_at - now

        before_messages = {
            10: "⏰ 모임 시작 10분 전입니다.",
            5: "⏰ 모임 시작 5분 전입니다.",
            1: "⏰ 모임 시작 1분 전입니다.",
        }

        for minutes, text in before_messages.items():
            if timedelta(minutes=minutes) <= diff < timedelta(minutes=minutes + 1):
                async_to_sync(channel_layer.group_send)(
                    room_group,
                    {
                        "type": "system_message",
                        "message": text,
                    }
                )

        # ▶️ 시작
        if timedelta(seconds=0) <= diff < timedelta(minutes=1):
            async_to_sync(channel_layer.group_send)(
                room_group,
                {
                    "type": "system_message",
                    "message": "▶️ 모임이 시작되었습니다!",
                }
            )

        # ⛔ 종료
        if timedelta(seconds=0) <= now - end_at < timedelta(minutes=1):
            async_to_sync(channel_layer.group_send)(
                room_group,
                {
                    "type": "system_message",
                    "message": "⛔ 모임이 종료되었습니다.",
                }
            )
