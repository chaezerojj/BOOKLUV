#!/bin/bash

# PYTHONPATH 설정
export PYTHONPATH=/code:$PYTHONPATH

echo "======================"
echo "Current working directory: $(pwd)"
echo "Server Type: $SERVER_TYPE"
echo "======================"

if [ "$SERVER_TYPE" = "HTTP" ]; then
    echo "Running Django migrations..."
    python manage.py migrate --noinput || { echo "Migration failed"; }

    echo "Collecting static files..."
    python manage.py collectstatic --noinput || { echo "Collectstatic failed"; }
fi

if [ "$SERVER_TYPE" = "HTTP" ]; then
    echo "Starting Gunicorn server for HTTP..."
    exec gunicorn backend.wsgi:application --bind 0.0.0.0:8000 --workers 3
    
elif [ "$SERVER_TYPE" = "WS" ]; then
    echo "Starting Daphne server for WebSockets..."
    exec daphne -b 0.0.0.0 -p 8001 backend.asgi:application
    
else
    echo "Error: SERVER_TYPE environment variable is not set (HTTP or WS)"
    exit 1
fi