#!/bin/bash
export PYTHONPATH=/app:$PYTHONPATH

# 빌드 타임인지 런타임인지 체크 (Railway는 빌드 시 PORT 변수가 없습니다)
if [ -z "$PORT" ]; then
    echo "== Build Stage: Skipping database operations =="
else
    echo "== Runtime Stage: Starting database operations =="

    # 1. DB 마이그레이션
    echo "Running Django migrations..."
    python manage.py migrate --noinput || { echo "Migration failed"; exit 1; }

    # 2. 데이터 이식 (PostgreSQL 연결 후 실행)
    if [ -f "data.json" ]; then
        echo "!!! data.json 발견: 데이터 임포트 시작 !!!"
        python manage.py loaddata data.json
    fi
fi

# 3. 정적 파일 수집 (이건 빌드 때 해도 무방합니다)
echo "Collecting static files..."
python manage.py collectstatic --noinput

# 4. 서버 실행
if [ -n "$PORT" ]; then
    echo "Starting Daphne on port $PORT..."
    exec daphne -b 0.0.0.0 -p $PORT backend.asgi:application
fi