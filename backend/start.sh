#!/bin/bash

export PYTHONPATH=/app:$PYTHONPATH

echo "Running Django migrations..."
python manage.py migrate --noinput

# --- 이 부분을 추가하세요 ---
if [ -f "data.json" ]; then
    echo "Found data.json, importing..."
    python manage.py loaddata data.json
fi
# --------------------------

echo "Starting Daphne server..."
exec daphne -b 0.0.0.0 -p $PORT backend.asgi:application