import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# 1분마다 실행하도록 스케줄 등록
app.conf.beat_schedule = {
    'create-rooms-every-minute': {
        'task': 'klub_talk.tasks.check_and_create_rooms',
        'schedule': 60.0,  # 초 단위 (여기선 60초마다)
    },
}
