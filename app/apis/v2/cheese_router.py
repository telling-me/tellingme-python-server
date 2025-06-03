from fastapi import APIRouter, status

from app.dtos.cheese.cheese_response import CheeseResponse, TotalCheeseAmount
from app.services.cheese_service import CheeseService
from app.services.user_service import UserService

cheese_router = APIRouter(prefix="/cheese", tags=["Cheese"])


@cheese_router.get("", response_model=CheeseResponse, status_code=status.HTTP_200_OK)
async def get_cheese_handler(user_id: str) -> CheeseResponse:
    user = await UserService.get_user_info(user_id=user_id)
    cheese_amount = await CheeseService.get_cheese_balance(user.cheese_manager_id)
    return CheeseResponse(
        code=status.HTTP_200_OK,
        message="총 치즈 갯수 조회",
        data=TotalCheeseAmount(cheeseBalance=cheese_amount),
    )
