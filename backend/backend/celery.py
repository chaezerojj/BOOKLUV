import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

app = Celery("backend")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

from celery.schedules import crontab

app.conf.beat_schedule = {
    "create_rooms_every_minute": {
        "task": "klub_talk.tasks.check_and_create_rooms",
        "schedule": 60.0,  # 1분마다 실행
    },
}
