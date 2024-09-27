# 1. 기본 Python 이미지를 지정합니다.
FROM python:3.12-slim

# 2. 작업 디렉토리를 설정합니다.
WORKDIR /app
ENV PYTHONPATH="/app/src"

# 3. 필수 패키지를 설치합니다.
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    wget \
    llvm \
    libncurses5-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libffi-dev \
    liblzma-dev \
    python3-openssl \
    default-libmysqlclient-dev \
    libmariadb-dev-compat \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 4. Poetry 설치
RUN curl -sSL https://install.python-poetry.org | python3 -

# 5. Poetry 환경 설정
ENV PATH="/root/.local/bin:$PATH"

# 6. 프로젝트 파일 복사 및 의존성 설치
COPY pyproject.toml poetry.lock /app/
RUN /bin/bash -c "source ~/.bashrc"
RUN /bin/bash -c "poetry config virtualenvs.create false"
RUN /bin/bash -c "poetry install --no-root"

# 7. 프로젝트 소스 코드 복사
COPY . /app

# 8. ENTRYPOINT 설정
RUN chmod +x ./scripts/start_app.sh
ENTRYPOINT ["/bin/bash", "./scripts/start_app.sh"]

# 9. Gunicorn이 8000 포트에서 수신하도록 EXPOSE
EXPOSE 8000