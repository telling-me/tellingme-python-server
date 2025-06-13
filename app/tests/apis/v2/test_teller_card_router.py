import asyncio

from fastapi import status

from app.common.constants.badge_code_list import BadgeCodeList
from app.common.constants.color_code_list import ColorCodeList
from app.common.exceptions.error_code import ErrorCode
from app.dtos.teller_card.teller_card_request import TellerCardRequest
from app.tests.mothers.badge_mother import BadgeMother
from app.tests.mothers.color_mother import ColorMother
from app.tests.mothers.user_mother import UserMother
from app.tests.telling_me_client import TellingMeClient


async def test_update_teller_card(telling_me_client: TellingMeClient, init_tortoise_connection: None) -> None:
    # Given
    user_mother = UserMother()
    badge_mother = BadgeMother()
    color_mother = ColorMother()

    user_id = await user_mother.create_user()

    await asyncio.gather(
        user_mother.create_level_inventory(),
        badge_mother.create_badge_inventory(),
        color_mother.create_color_inventory(),
        badge_mother.create_badge(user_id=user_id, badge_code=BadgeCodeList.FIRST),
    )

    teller_card_request = TellerCardRequest(
        user_id=user_id,
        badgeCode=BadgeCodeList.FIRST,
        colorCode=ColorCodeList.CL_RED_001,
    )

    # When
    before_update_response = await telling_me_client.get_mobile_teller_card(user_id=user_id)
    before_user_data = before_update_response.json()["data"]["userInfo"]["tellerCard"]

    update_response = await telling_me_client.update_teller_card(teller_card_request=teller_card_request)

    after_update_response = await telling_me_client.get_mobile_teller_card(user_id=user_id)
    after_user_data = after_update_response.json()["data"]["userInfo"]["tellerCard"]

    # Then
    assert before_update_response.status_code == status.HTTP_200_OK
    assert update_response.status_code == status.HTTP_200_OK
    assert after_update_response.status_code == status.HTTP_200_OK

    assert before_user_data["colorCode"] == ColorCodeList.CL_DEFAULT
    assert before_user_data["badgeCode"] == BadgeCodeList.NEW

    assert after_user_data["colorCode"] == ColorCodeList.CL_RED_001
    assert after_user_data["badgeCode"] == BadgeCodeList.FIRST


async def test_update_teller_card_with_invalid_code(
    telling_me_client: TellingMeClient, init_tortoise_connection: None
) -> None:
    # Given
    user_mother = UserMother()
    badge_mother = BadgeMother()
    color_mother = ColorMother()

    user_id = await user_mother.create_user()
    await asyncio.gather(
        user_mother.create_level_inventory(),
        badge_mother.create_badge_inventory(),
        color_mother.create_color_inventory(),
        badge_mother.create_badge(user_id=user_id, badge_code=BadgeCodeList.FIRST),
    )

    invalid_badge_code_request = TellerCardRequest(
        user_id=user_id,
        badgeCode="invalid_badge_code",
        colorCode=ColorCodeList.CL_RED_001,
    )
    invalid_color_code_request = TellerCardRequest(
        user_id=user_id,
        badgeCode=BadgeCodeList.FIRST,
        colorCode="invalid_color_code",
    )

    # When
    invalid_badge_code_response = await telling_me_client.update_teller_card(
        teller_card_request=invalid_badge_code_request
    )
    invalid_color_code_response = await telling_me_client.update_teller_card(
        teller_card_request=invalid_color_code_request
    )

    # Then
    assert invalid_badge_code_response.status_code == status.HTTP_400_BAD_REQUEST
    assert invalid_color_code_response.status_code == status.HTTP_400_BAD_REQUEST

    assert invalid_badge_code_response.json()["message"] == ErrorCode.INVALID_BADGE_CODE.message
    assert invalid_color_code_response.json()["message"] == ErrorCode.INVALID_COLOR_CODE.message
