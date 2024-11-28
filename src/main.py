import logging

from fastapi import FastAPI

from common.post_construct import post_construct
from core.configs import settings

logging.basicConfig(level=logging.DEBUG)

db_client_logger = logging.getLogger("tortoise.db_client")
db_client_logger.setLevel(logging.DEBUG)

app = FastAPI()
print(settings.APPLE_URL)
print(settings.APPLE_SHARED_SECRET)

post_construct(app)


@app.get("/health_check")
def health_check() -> dict[str, str]:
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
