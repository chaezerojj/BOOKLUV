#!/bin/bash
export PYTHONPATH=/app:$PYTHONPATH

# 정적 파일만 수집 (이건 빠릅니다)
echo "Collecting static files..."
python manage.py collectstatic --noinput

# 서버 실행 (Daphne)
echo "Starting Daphne..."
exec daphne -b 0.0.0.0 -p ${PORT:-8080} backend.asgi:application