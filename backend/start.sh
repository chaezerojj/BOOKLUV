#!/bin/bash

export PYTHONPATH=$PYTHONPATH:$(pwd)

echo "======================"
echo "Current working directory: $(pwd)"
echo "Server Type: $SERVER_TYPE"
echo "======================"

if [ "$SERVER_TYPE" = "HTTP" ]; then
    echo "Running Django migrations..."
    python manage.py migrate --noinput
    
    echo "Starting Gunicorn..."
    exec gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT --workers 3

elif [ "$SERVER_TYPE" = "WS" ]; then
    echo "Starting Daphne..."
    exec daphne -b 0.0.0.0 -p $PORT backend.asgi:application

# ✅ Celery 워커 + 비트 케이스 추가
elif [ "$SERVER_TYPE" = "CELERY" ]; then
    echo "Starting Celery Worker with Beat..."
    # -B 옵션으로 워커와 스케줄러를 동시에 실행
    exec celery -A backend worker -l info -B

else
    echo "Error: SERVER_TYPE must be HTTP, WS, or CELERY"
    exit 1
fi