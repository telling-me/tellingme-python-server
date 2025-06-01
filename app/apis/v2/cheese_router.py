from fastapi import APIRouter, status

from app.dtos.cheese.cheese_dto import CheeseResponseDTO
from app.services.cheese_service import CheeseService
from app.services.user_service import UserService

cheese_router = APIRouter(prefix="/cheese", tags=["Cheese"])


@cheese_router.get("", response_model=CheeseResponseDTO, status_code=status.HTTP_200_OK)
async def get_cheese_handler(user_id: str) -> CheeseResponseDTO:

    user = await UserService.get_user_info(user_id=user_id)
    cheese_amount = await CheeseService.get_cheese_balance(user["cheese_manager_id"])
    print(cheese_amount)

    return CheeseResponseDTO.builder(cheese_balance=cheese_amount)
