#!/bin/bash

# 변수가 없으면 기본값 WS
SERVER_TYPE=${SERVER_TYPE:-WS}
export PYTHONPATH=$PYTHONPATH:$(pwd)

echo "======================"
echo "Server Type: $SERVER_TYPE"
echo "======================"

if [ "$SERVER_TYPE" = "HTTP" ]; then
    echo "Running Django migrations..."
    python manage.py migrate --noinput
    exec gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT --workers 3

elif [ "$SERVER_TYPE" = "WS" ]; then
    echo "Starting Celery..."
    # 로그를 파일로 돌리지 않고 바로 출력 (stdout/stderr)
    celery -A backend worker -l info -B & 
    
    echo "Starting Daphne..."
    exec daphne -b 0.0.0.0 -p $PORT backend.asgi:application
    
elif [ "$SERVER_TYPE" = "CELERY" ]; then
    echo "Starting Celery Worker with Beat..."
    exec celery -A backend worker -l info -B
fi