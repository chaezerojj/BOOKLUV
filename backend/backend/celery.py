# backend/celery.py

import os
from celery import Celery

# Django settings 모듈을 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Celery 애플리케이션을 생성
app = Celery('backend')

# Celery 설정을 Django settings에서 로드
app.config_from_object('django.conf:settings', namespace='CELERY')

# 자동으로 앱의 tasks.py 파일을 로드
app.autodiscover_tasks(['klub_talk'])

# Beat 스케줄 설정: 1분마다 Room 생성, 회의 알람 체크
app.conf.beat_schedule = {
    'create-rooms-every-minute': {
        'task': 'klub_talk.tasks.check_and_create_rooms',
        'schedule': 60.0,  # 1분마다 실행
    },
    'send-today-meeting-alarms': {
        'task': 'klub_talk.tasks.send_today_meeting_alarms',  # 알람 보내기
        'schedule': 60.0,  # 1분마다 실행
    },
}

# Celery 애플리케이션을 호출 가능한 객체로 설정
app.conf.timezone = 'Asia/Seoul'
