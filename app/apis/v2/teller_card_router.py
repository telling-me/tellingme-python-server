from fastapi import APIRouter, status

from app.dtos.teller_card.request import TellerCardRequestDTO
from app.dtos.teller_card.response import TellerCardResponseDTO
from app.services.teller_card_service import TellerCardService

teller_card_router = APIRouter(prefix="/tellercard", tags=["TellerCard"])


@teller_card_router.post(
    "",
    response_model=TellerCardResponseDTO,
    status_code=status.HTTP_200_OK,
)
async def patch_teller_card_handler(
    body: TellerCardRequestDTO,
) -> TellerCardResponseDTO:
    user_id = body.user_id
    badge_code = body.badgeCode
    color_code = body.colorCode

    await TellerCardService.validate_teller_card(badge_code=badge_code, color_code=color_code)

    await TellerCardService.patch_teller_card(user_id=user_id, badge_code=badge_code, color_code=color_code)

    teller_card = await TellerCardService.get_teller_card(user_id=user_id)

    return TellerCardResponseDTO.builder(teller_card=teller_card)
