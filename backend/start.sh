#!/bin/bash

# 1. PYTHONPATH 설정
export PYTHONPATH=/app:$PYTHONPATH

echo "======================"
echo "Starting Start Script..."
echo "======================"

# 2. DB 마이그레이션
echo "Running Django migrations..."
python manage.py migrate --noinput || { echo "Migration failed"; exit 1; }

# 3. 데이터 이식 (이미 성공했다면 건너뛰게 됩니다)
if [ -f "data.json" ]; then
    echo "Found data.json, importing..."
    python manage.py loaddata data.json
fi

# 4. 정적 파일 수집
echo "Collecting static files..."
python manage.py collectstatic --noinput

# 5. 서버 실행 (Daphne 명령어 완전 교정)
# 포트 번호 변수 앞에 -p를 붙이고, 앱 위치는 맨 뒤로 보냅니다.
echo "Starting Daphne on port ${PORT:-8080}..."
exec daphne -b 0.0.0.0 -p ${PORT:-8080} backend.asgi:application