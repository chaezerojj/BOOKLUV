#!/bin/bash

# 1. PYTHONPATH 설정
export PYTHONPATH=/app:$PYTHONPATH

echo "======================"
echo "DB 연결 확인 및 마이그레이션 시작"
echo "======================"

# 2. DB 테이블 생성 (이제 진짜 Postgres에 테이블이 생깁니다)
python manage.py migrate --noinput || { echo "Migration failed"; exit 1; }

# 3. 데이터 이식 (PostgreSQL로 126개 데이터를 넣습니다)
if [ -f "data.json" ]; then
    echo "Found data.json, importing..."
    python manage.py loaddata data.json
fi

# 4. 정적 파일 수집
echo "Collecting static files..."
python manage.py collectstatic --noinput

# 5. 서버 실행 (Daphne 명령어 위치 수정 완료)
echo "Starting Daphne on port ${PORT:-8080}..."
exec daphne -b 0.0.0.0 -p ${PORT:-8080} backend.asgi:application