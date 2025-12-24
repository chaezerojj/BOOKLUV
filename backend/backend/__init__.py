# backend/__init__.py

from __future__ import absolute_import, unicode_literals
from .celery import app as celery_app
from klub_talk.tasks import *
# 이 모듈이 임포트될 때 Celery 앱을 자동으로 불러오기
__all__ = ('celery_app',)
