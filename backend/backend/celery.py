import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(['klub_talk'])

# Beat 스케줄 설정
app.conf.beat_schedule = {
    'create-rooms-every-minute': {
        'task': 'backend.klub_talk.tasks.check_and_create_rooms',
        'schedule': 10.0,
    },
    'send_today_meeting_alarms_for_today': {
        'task': 'backend.klub_talk.tasks.send_today_meeting_alarms_for_today',
        'schedule': 10.0,
    },
    "send_meeting_system_messages": {
        "task": "backend.klub_talk.tasks.send_meeting_system_messages",
        'schedule': 10.0,
    },
}

app.conf.timezone = 'Asia/Seoul'

# 🔹 worker 시작 시 task를 강제로 import
from klub_talk import tasks
