#!/bin/bash

# 변수가 없으면 기본값 WS
SERVER_TYPE=${SERVER_TYPE:-WS}
export PYTHONPATH=$PYTHONPATH:$(pwd)
export PYTHONUNBUFFERED=1

echo "======================"
echo "Server Type: $SERVER_TYPE"
echo "======================"

if [ "$SERVER_TYPE" = "HTTP" ]; then
    echo "Running Django migrations..."
    python manage.py migrate --noinput
    exec gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT --workers 3

elif [ "$SERVER_TYPE" = "WS" ]; then
    echo "Starting Celery Worker & Beat (Light Mode)..."
    celery -A backend worker -l info -B --schedule=/tmp/celerybeat-schedule --pidfile= --concurrency=1 --max-tasks-per-child=10 & 
    
    echo "Starting Daphne..."
    exec daphne -b 0.0.0.0 -p $PORT backend.asgi:application
    
elif [ "$SERVER_TYPE" = "CELERY" ]; then
    echo "Starting Celery Worker with Beat (Standalone Mode)..."
    exec celery -A backend worker -l info -B --schedule=/tmp/celerybeat-schedule --pidfile= --concurrency=1 --max-tasks-per-child=10
fi