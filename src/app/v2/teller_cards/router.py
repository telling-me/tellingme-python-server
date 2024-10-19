from fastapi import APIRouter, status

from app.v2.badges.models.badge import Badge
from app.v2.teller_cards.dtos.response import TellerCardResponseDTO
from app.v2.teller_cards.dtos.request import TellerCardRequestDTO
from app.v2.teller_cards.models.teller_card import TellerCard


router = APIRouter(prefix="/tellercard", tags=["TellerCard"])


@router.patch(
    "/",
    response_model=TellerCardResponseDTO,
    status_code=status.HTTP_200_OK,
)
async def patch_teller_card_handler(
    body: TellerCardRequestDTO,
) -> TellerCardResponseDTO:
    user_id = "180a4e40-62f8-46be-b1eb-e7e3dd91cddf"
    badge_code = (body.badgeCode,)
    color_code = (body.colorCode,)

    await TellerCard.patch_teller_card_info_by_user_id(
        user_id=user_id,
        badge_code=badge_code,
        color_code=color_code,
    )

    teller_card = await TellerCard.get_teller_card_info_by_user_id(user_id=user_id)
    print(teller_card)

    await Badge.get_badge_count_and_codes_by_user_id(user_id)
    return TellerCardResponseDTO(
        colorCode=body.colorCode,
        badgeCode=body.badgeCode,
    )
