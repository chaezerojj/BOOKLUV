# klub_talk/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from django.utils import timezone
from klub_talk.models import Meeting

@receiver(post_save, sender=Meeting)
def schedule_meeting_alarm(sender, instance, created, raw, **kwargs):
    if raw:
        return
    if created:
        alarm_time = instance.started_at - timedelta(minutes=10)
        if alarm_time > timezone.now():
            # task import를 여기서
            from klub_talk.tasks import send_today_meeting_alarms_for_today
            send_today_meeting_alarms_for_today.apply_async(eta=alarm_time)
