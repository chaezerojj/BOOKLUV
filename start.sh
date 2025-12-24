#!/bin/bash

echo "Running Django migrations..."
python3 manage.py migrate || { echo "Django migration failed"; exit 1; }

echo "Starting Django server..."
python3 manage.py runserver 0.0.0.0:8000 || { echo "Django server failed"; exit 1; }

echo "Starting Celery worker..."
celery -A backend worker -l info || { echo "Celery worker failed"; exit 1; }

echo "Starting Celery Beat..."
celery -A backend beat -l info || { echo "Celery Beat failed"; exit 1; }
