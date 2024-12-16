from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from common.exceptions.custom_exception import CustomException


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

    @app.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException) -> JSONResponse:
        status_code = exc.error_code.code // 10
        return JSONResponse(
            status_code=status_code,
            content=exc.to_dict(),
        )
