#!/bin/bash
export PYTHONPATH=/app:$PYTHONPATH

echo "== Django Migration =="
python manage.py migrate --noinput || { echo "Migration failed"; exit 1; }

if [ -f "data.json" ]; then
    echo "== Importing Data =="
    python manage.py loaddata data.json
fi

echo "== Collecting Static =="
python manage.py collectstatic --noinput

echo "== Starting Daphne =="
exec daphne -b 0.0.0.0 -p ${PORT:-8080} backend.asgi:application