#!/bin/bash
export PYTHONPATH=/app:$PYTHONPATH

# 빌드할 때나 실행할 때 정적 파일만 준비합니다.
echo "Collecting static files..."
python manage.py collectstatic --noinput

# 서버 실행
echo "Starting Daphne server..."
exec daphne -b 0.0.0.0 -p ${PORT:-8080} backend.asgi:application