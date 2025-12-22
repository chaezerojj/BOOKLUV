from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from django.utils import timezone

from klub_talk.models import Meeting
from klub_talk.tasks import send_today_meeting_alarms


@receiver(post_save, sender=Meeting)
def schedule_meeting_alarm(sender, instance, created, raw, **kwargs):
    # 🚨 fixture / loaddata / migrate 중이면 아무것도 하지 않음
    if raw:
        return

    if created:
        alarm_time = instance.started_at - timedelta(minutes=10)
        if alarm_time > timezone.now():
            send_today_meeting_alarms.apply_async(eta=alarm_time)
