cat deploy-prod.sh
#!/bin/bash

# src 디렉토리로 이동
cd "$(dirname "$0")/../src" || exit

# .env.prod 파일 확인 및 로드
if [ ! -f .env.prod ]; then
  echo ".env.prod file not found in src directory. Exiting."
  exit 1
fi
echo "Loading environment variables from src/.env.prod..."
export $(grep -v '^#' .env.prod | xargs)

# 실행 중인 Gunicorn 프로세스 종료
echo "Stopping Gunicorn..."
killall gunicorn 2>/dev/null || echo "No Gunicorn processes found."

# 실행 중인 Celery 워커 프로세스 종료
echo "Stopping Celery workers..."
pkill -f "celery -A celery_worker worker" 2>/dev/null || echo "No Celery worker processes found."

# 새로운 Celery 워커 시작
echo "Starting Celery workers..."
PYTHONPATH=$(pwd) /home/ubuntu/.cache/pypoetry/virtualenvs/tellingme-python-server-p3Rjg27q-py3.12/bin/python -m celery -A celery_worker worker --loglevel=info --concurrency=1 &

if pgrep -f "celery -A celery_worker worker" > /dev/null; then
  echo "Celery worker started successfully."
else
  echo "Failed to start Celery worker."
  exit 1
fi

# 새로운 Gunicorn 시작
echo "Starting Gunicorn..."
ENV=prod poetry run nohup gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 &

if pgrep gunicorn > /dev/null; then
  echo "Gunicorn server started successfully."
else
  echo "Failed to start Gunicorn server."
  exit 1
fi