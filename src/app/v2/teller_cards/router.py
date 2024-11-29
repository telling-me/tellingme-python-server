from fastapi import APIRouter, status

from app.v2.teller_cards.dtos.request import TellerCardRequestDTO
from app.v2.teller_cards.dtos.response import TellerCardResponseDTO
from app.v2.teller_cards.services.teller_card_service import TellerCardService

router = APIRouter(prefix="/tellercard", tags=["TellerCard"])


@router.post(
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
