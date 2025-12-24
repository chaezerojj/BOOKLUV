#!/bin/bash

# Django 마이그레이션 실행
echo "Running Django migrations..."
python manage.py migrate

# Django 서버 실행
echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000 &  # 백그라운드 실행

# Celery 워커 실행
echo "Starting Celery worker..."
celery -A backend worker -l info &  # 백그라운드 실행

# Celery Beat 실행
echo "Starting Celery Beat..."
celery -A backend beat -l info &  # 백그라운드 실행

wait  # 모든 백그라운드 프로세스가 끝날 때까지 기다림
