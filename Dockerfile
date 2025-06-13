# Redis 공식 이미지 사용
FROM redis:7.2-alpine

# 포트 오픈
EXPOSE 6379


# 기본 명령 실행 (기본 설정 사용 시)
CMD ["redis-server"]
# 커스텀 설정 사용 시 아래 명령어 사용
# CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]

# 빌드 명령어
# docker build -t my-redis .

# 컨테이너 실행 명령어
# docker run -d -p 6379:6379 --name redis-server my-redis
