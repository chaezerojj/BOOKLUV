#!/bin/bash

# 시작 메시지
echo "Starting the backend services..."

# Django 마이그레이션 실행
echo "Running Django migrations..."
python3 manage.py migrate

# Django 서버 실행 (0.0.0.0은 외부에서 접근 가능하게 설정)
echo "Starting Django server..."
python3 manage.py runserver 0.0.0.0:8000

# Celery 워커 실행
echo "Starting Celery worker..."
celery -A backend worker -l info &

# Celery Beat 실행
echo "Starting Celery Beat..."
celery -A backend beat -l info &
