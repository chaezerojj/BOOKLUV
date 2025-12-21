import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')

# Django settings에서 Celery 설정을 로드
app.config_from_object('django.conf:settings', namespace='CELERY')

# 자동으로 'klub_talk' 앱의 tasks.py 파일을 로드
app.autodiscover_tasks(['klub_talk'])

# Beat 스케줄: 1분마다 Room 생성, 회의 알람 체크
app.conf.beat_schedule = {
    'create-rooms-every-minute': {
        'task': 'klub_talk.tasks.check_and_create_rooms',
        'schedule': 60.0,  # 1분마다
    },
    'send_today_meeting_alarms': {
        'task': 'klub_talk.tasks.send_today_meeting_alarms',  # 이름 수정
        'schedule': 60.0,  # 1분마다
    },
}
