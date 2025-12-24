#!/bin/bash

# 1. PYTHONPATH 설정
export PYTHONPATH=/app:$PYTHONPATH

echo "======================"
echo "Current working directory: $(pwd)"
echo "Starting BookLuv Production Server..."
echo "======================"

# 2. DB 마이그레이션 (테이블 구조 유지 확인)
echo "Checking for pending migrations..."
python manage.py migrate --noinput || { echo "Migration failed"; exit 1; }

# 3. 정적 파일 수집 (CSS/JS 등 서빙 준비)
echo "Collecting static files..."
python manage.py collectstatic --noinput || { echo "Collectstatic failed"; exit 1; }

# 4. 서버 실행 (Daphne 명령어 수정 완료)
# backend.asgi:application (콜론 사용) 형식이 가장 안정적입니다.
echo "Starting Daphne server for WebSockets on port ${PORT:-8080}..."
exec daphne -b 0.0.0.0 -p ${PORT:-8080} backend.asgi:application