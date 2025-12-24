#!/bin/bash

# PYTHONPATH 설정
export PYTHONPATH=/app:$PYTHONPATH

echo "======================"
echo "Current working directory: $(pwd)"
echo "======================"

# start.sh 수정 (예시)
echo "Running Django migrations..."
python manage.py migrate --noinput --fake-initial || { echo "Migration failed but continuing..."; }

# 2. 정적 파일 수집
echo "Collecting static files..."
python manage.py collectstatic --noinput || { echo "Collectstatic failed"; exit 1; }

# 3. 서버 실행 (Gunicorn + Uvicorn worker 조합 또는 Daphne) 
# 여기서는 웹소켓 처리가 가능한 Daphne를 사용합니다.
echo "Starting Daphne server for WebSockets..."
exec daphne -b 0.0.0.0 -p $PORT backend.asgi:application