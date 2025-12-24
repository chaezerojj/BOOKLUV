#!/bin/sh
set -e

echo "Running Django migrations..."
python3 manage.py migrate

echo "Collecting static files..."
python3 manage.py collectstatic --noinput

echo "Starting Django server..."
python3 manage.py runserver 0.0.0.0:${PORT:-8000}
