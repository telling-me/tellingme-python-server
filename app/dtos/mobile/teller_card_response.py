from app.dtos.base_response import BaseResponseDTO
from app.dtos.frozen_config import FROZEN_CONFIG
from app.dtos.mobile.data_dto import DataDTO


# 최종 응답 DTO
class TellerCardResponse(BaseResponseDTO):
    model_config = FROZEN_CONFIG

    data: DataDTO
