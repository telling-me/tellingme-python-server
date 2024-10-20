from fastapi import APIRouter, status

from app.v2.cheese_managers.dtos.cheese_dto import CheeseResponseDTO
from app.v2.cheese_managers.services.cheese_service import CheeseService
from app.v2.users.services.user_service import UserService

router = APIRouter(prefix="/cheese", tags=["Cheese"])


@router.get("", response_model=CheeseResponseDTO, status_code=status.HTTP_200_OK)
async def get_cheese_handler():
    user_id = "180a4e40-62f8-46be-b1eb-e7e3dd91cddf"
    user = await UserService.get_user_info(user_id=user_id)
    cheese_amount = await CheeseService.get_cheese_balance(user["cheese_manager_id"])

    return CheeseResponseDTO.builder(cheese_balance=cheese_amount)
