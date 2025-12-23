import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(['klub_talk'])

# Beat 스케줄 설정
app.conf.beat_schedule = {
    'create-rooms-every-minute': {
        'task': 'klub_talk.tasks.check_and_create_rooms',
        'schedule': 10.0,
    },
    'send_today_meeting_alarms_for_today': {
        'task': 'klub_talk.tasks.send_today_meeting_alarms_for_today',
        'schedule': 10.0,
    },
}

app.conf.timezone = 'Asia/Seoul'

# 🔹 worker 시작 시 task를 강제로 import
import klub_talk.tasks
