from typing import Any, Optional

from pydantic import BaseModel

from app.dtos.frozen_config import FROZEN_CONFIG


# 공통 응답 모델 정의
class BaseResponseDTO(BaseModel):
    model_config = FROZEN_CONFIG

    code: int
    message: str
    data: Optional[Any] = None
