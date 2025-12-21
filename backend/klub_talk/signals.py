from django.db.models.signals import post_save
from django.dispatch import receiver
from klub_talk.models import Meeting
from datetime import timedelta
from django.utils import timezone
from klub_talk.tasks import send_today_meeting_alarms

@receiver(post_save, sender=Meeting)
def schedule_meeting_alarm(sender, instance, created, **kwargs):
    if created:
        alarm_time = instance.started_at - timedelta(minutes=10)
        if alarm_time > timezone.now():
            send_today_meeting_alarms.apply_async(eta=alarm_time)
