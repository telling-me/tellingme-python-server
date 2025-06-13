import asyncio

from fastapi import status

from app.common.constants.badge_code_list import BadgeCodeList
from app.tests.mothers.badge_mother import BadgeMother
from app.tests.mothers.user_mother import UserMother
from app.tests.telling_me_client import TellingMeClient


async def test_get_badges(telling_me_client: TellingMeClient, init_tortoise_connection: None) -> None:
    # Given
    user_mother = UserMother()
    badge_mother = BadgeMother()

    user_id = await user_mother.create_user()
    await asyncio.gather(
        badge_mother.create_badge_inventory(), badge_mother.create_badge(user_id=user_id, badge_code=BadgeCodeList.NEW)
    )

    # When
    response = await telling_me_client.get_badges(user_id=user_id)
    code = response.json()["code"]
    data = response.json()["data"]
    message = response.json()["message"]

    # Then
    assert response.status_code == status.HTTP_200_OK

    assert code == response.status_code
    assert message == "보유 뱃지 정보 조회"
    assert data[0]["badgeCode"] == BadgeCodeList.NEW
    assert data[0]["badgeName"] == "미스터리 방문객"
    assert data[0]["badgeMiddleName"] == "아직은 낯설어요,"
    assert data[0]["badgeCondition"] == "회원가입 시 기본 제공"
