#!/bin/bash

# PYTHONPATH 설정
export PYTHONPATH=/app:$PYTHONPATH

echo "======================"
echo "Current working directory: $(pwd)"
echo "Listing files to check for data.json:"
ls -al
echo "======================"

# 1. DB 마이그레이션
echo "Running Django migrations..."
python manage.py migrate --noinput || { echo "Migration failed"; exit 1; }

# 2. 데이터 이식 (data.json 파일이 있을 때만 실행)
if [ -f "data.json" ]; then
    echo "--------------------------------"
    echo "!!! data.json 발견: PostgreSQL로 데이터를 옮깁니다 !!!"
    python manage.py loaddata data.json || { echo "Data import failed"; exit 1; }
    echo "!!! 데이터 임포트 성공 !!!"
    echo "--------------------------------"
fi

# 3. 정적 파일 수집
echo "Collecting static files..."
python manage.py collectstatic --noinput || { echo "Collectstatic failed"; exit 1; }

# 4. 서버 실행
echo "Starting Daphne server for WebSockets..."
exec daphne -b 0.0.0.0 -p $PORT backend.asgi:application