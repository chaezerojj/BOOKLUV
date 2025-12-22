# backend/__init__.py

from __future__ import absolute_import, unicode_literals

# Celery 애플리케이션을 불러오기
from .celery import app as celery_app

# 이 모듈이 임포트될 때 Celery 앱을 자동으로 불러오기
__all__ = ('celery_app',)
