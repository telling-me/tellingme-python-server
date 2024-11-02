from fastapi import APIRouter, status

from app.v2.teller_cards.dtos.response import TellerCardResponseDTO
from app.v2.teller_cards.dtos.request import TellerCardRequestDTO

from app.v2.teller_cards.services.teller_card_service import TellerCardService

router = APIRouter(prefix="/tellercard", tags=["TellerCard"])


@router.patch(
    "",
    response_model=TellerCardResponseDTO,
    status_code=status.HTTP_200_OK,
)
async def patch_teller_card_handler(
    body: TellerCardRequestDTO,
) -> TellerCardResponseDTO:
    user_id = "180a4e40-62f8-46be-b1eb-e7e3dd91cddf"
    badge_code = (body.badgeCode,)
    color_code = (body.colorCode,)

    await TellerCardService.patch_teller_card(
        user_id=user_id, badge_code=badge_code, color_code=color_code
    )

    teller_card = await TellerCardService.get_teller_card(user_id=user_id)

    activate_badge_code = teller_card["activate_badge_code"]
    activate_color_code = teller_card["activate_color_code"]

    return TellerCardResponseDTO(
        colorCode=activate_color_code,
        badgeCode=activate_badge_code,
    )
