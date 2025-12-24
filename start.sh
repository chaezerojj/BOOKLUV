#!/bin/bash
# 백엔드 서버 실행 명령어

# Django 서버 실행
echo "Starting Django server..."
python manage.py migrate  # 마이그레이션 실행
python manage.py runserver 0.0.0.0:8000  # Django 서버 실행 (0.0.0.0은 모든 외부 요청을 받도록 설정)

# WebSocket, Redis와 같은 서비스가 도커에서 이미 설정되어 있어야 함
