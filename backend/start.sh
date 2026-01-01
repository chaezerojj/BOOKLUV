#!/bin/bash

SERVER_TYPE=${SERVER_TYPE:-WS}
export PYTHONPATH=$PYTHONPATH:$(pwd)
export PYTHONUNBUFFERED=1

echo "======================"
echo "Server Type: $SERVER_TYPE"
echo "======================"

if [ "$SERVER_TYPE" = "HTTP" ]; then
    python manage.py migrate --noinput
    exec gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT --workers 3

elif [ "$SERVER_TYPE" = "WS" ]; then
    echo "1. Starting Daphne first (Priority)..."
    daphne -b 0.0.0.0 -p $PORT backend.asgi:application &
    
    echo "2. Waiting for Daphne to settle..."
    sleep 5
    
    echo "3. Starting Celery Worker & Beat (Lightest Mode)..."
    exec celery -A backend worker -l info -B --schedule=/tmp/celerybeat-schedule --pidfile= --concurrency=1 --prefetch-multiplier=1

elif [ "$SERVER_TYPE" = "CELERY" ]; then
    echo "Starting Standalone Celery..."
    exec celery -A backend worker -l info -B --schedule=/tmp/celerybeat-schedule --pidfile= --concurrency=1
fi