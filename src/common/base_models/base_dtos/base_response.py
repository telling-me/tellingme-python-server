from pydantic import BaseModel
from typing import Any, Optional


# 공통 응답 모델 정의
class BaseResponseDTO(BaseModel):
    code: int
    message: str
    data: Optional[Any] = None
