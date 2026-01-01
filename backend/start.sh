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
    echo "Starting Celery (Worker + Beat)..."
    # ✅ 에러를 유발하던 --broker 옵션을 삭제했습니다. 
    # 이제 settings.py의 CELERY_BROKER_URL을 자동으로 읽어옵니다.
    celery -A backend worker -l info -B & 
    
    echo "Starting Daphne..."
    exec daphne -b 0.0.0.0 -p $PORT backend.asgi:application
    
elif [ "$SERVER_TYPE" = "CELERY" ]; then
    echo "Starting Celery Worker with Beat..."
    exec celery -A backend worker -l info -B
fi