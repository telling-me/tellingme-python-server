from fastapi import APIRouter, status

from app.dtos.teller_card.teller_card_request import TellerCardRequest
from app.dtos.teller_card.teller_card_response import TellerCardResponse
from app.services.teller_card_service import TellerCardService

teller_card_router = APIRouter(prefix="/tellercard", tags=["TellerCard"])


@teller_card_router.post(
    "",
    response_model=TellerCardResponse,
    status_code=status.HTTP_200_OK,
)
async def patch_teller_card_handler(
    teller_card_request: TellerCardRequest,
) -> TellerCardResponse:
    return TellerCardResponse(
        code=status.HTTP_200_OK,
        message="success",
        data=await TellerCardService.patch_teller_card(
            user_id=teller_card_request.user_id,
            badge_code=teller_card_request.badgeCode,
            color_code=teller_card_request.colorCode,
        ),
    )


# todo : teller card, mission, mobile refactoring 및 purchase 삭제 및 테스트 코드 작성
