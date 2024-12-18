#!/bin/bash

# src 디렉토리로 이동
cd "$(dirname "$0")/../src" || exit

# 실행 중인 Gunicorn 프로세스 종료
echo "Stopping Gunicorn..."
killall gunicorn 2>/dev/null || echo "No Gunicorn processes found."

# 실행 중인 Celery 워커 프로세스 종료
echo "Stopping Celery workers..."
pkill -f "celery -A celery_worker worker" 2>/dev/null || echo "No Celery worker processes found."

# 새로운 Celery 워커 시작
echo "Starting Celery workers..."
PYTHONPATH=$(pwd) /home/ubuntu/.cache/pypoetry/virtualenvs/tellingme-python-server-p3Rjg27q-py3.12/bin/python -m celery -A celery_worker worker --loglevel=info --concurrency=1 &

# 새로운 Gunicorn 시작
echo "Starting Gunicorn..."
poetry run nohup gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 >> gunicorn.log 2>&1 &

echo "Services restarted successfully."