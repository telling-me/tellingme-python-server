#!/bin/bash

export PYTHONPATH=src
poetry install --no-root

# FastAPI 애플리케이션을 Gunicorn으로 실행
# -k uvicorn.workers.UvicornWorker: Uvicorn 워커를 사용하여 FastAPI를 실행
# -w: 워커 수를 지정 (CPU 코어 수에 맞춰 조정)
# -b: 바인딩할 주소 및 포트
# src.main:app -> src 디렉토리 내의 main.py 파일에서 "app" 객체를 가리킴 (FastAPI 인스턴스)

exec gunicorn -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 main:app