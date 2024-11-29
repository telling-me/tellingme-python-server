from fastapi import FastAPI, Request
from starlette.responses import JSONResponse


def attach_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={
                "code": 500,
                "data": str(exc),
                "message": "An unexpected error occurred. Please try again later.",
            },
        )
