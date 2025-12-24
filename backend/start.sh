#!/bin/bash
export PYTHONPATH=/app:$PYTHONPATH

# 빌드 시점에는 정적 파일만 수집
python manage.py collectstatic --noinput

# 서버 실행 (Daphne)
exec daphne -b 0.0.0.0 -p ${PORT:-8080} backend.asgi:application