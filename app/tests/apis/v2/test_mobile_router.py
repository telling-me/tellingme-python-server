import asyncio
from datetime import datetime

import time_machine
from fastapi import status

from app.common.constants.badge_code_list import BadgeCodeList
from app.common.constants.color_code_list import ColorCodeList
from app.core.configs import settings
from app.tests.mothers.answer_mother import AnswerMother
from app.tests.mothers.badge_mother import BadgeMother
from app.tests.mothers.color_mother import ColorMother
from app.tests.mothers.user_mother import UserMother
from app.tests.telling_me_client import TellingMeClient


async def test_get_mobile_teller_card(telling_me_client: TellingMeClient, init_tortoise_connection: None) -> None:
    # Given
    user_mother = UserMother()
    answer_mother = AnswerMother()
    badge_mother = BadgeMother()
    color_mother = ColorMother()

    user_id = await user_mother.create_user(user_name=(user_name := "telling me user"))

    await asyncio.gather(
        user_mother.create_level_inventory(),
        badge_mother.create_badge_inventory(),
        color_mother.create_color_inventory(),
        answer_mother.create_answer(user_id=user_id, content="-", date="2025-06-10"),
        answer_mother.create_answer(user_id=user_id, content="-", date="2025-06-12"),
        answer_mother.create_answer(user_id=user_id, content="-", date="2025-06-13"),
        user_mother.add_cheese(user_id=user_id, amount=(cheese_amount := 100)),
        badge_mother.create_badge(user_id=user_id, badge_code=BadgeCodeList.FIRST),
    )

    excepted_badges = [
        {
            "badgeCode": BadgeCodeList.FIRST,
            "badgeName": "탐험가 텔러",
            "badgeMiddleName": "낯선 길에 첫 발자국,",
            "badgeCondition": "첫 글을 작성했어요!",
        }
    ]
    expected_colors = [
        {"colorCode": ColorCodeList.CL_BLUE_001, "colorName": "Blue_1", "colorHexCode": "#229DF6"},
        {"colorCode": ColorCodeList.CL_DEFAULT, "colorName": "Default", "colorHexCode": "#1EDCC5"},
        {"colorCode": ColorCodeList.CL_ORANGE_001, "colorName": "Orange_1", "colorHexCode": "#FFA216"},
        {"colorCode": ColorCodeList.CL_RED_001, "colorName": "Red_1", "colorHexCode": "#ED3639"},
    ]

    # When
    with time_machine.travel(datetime(2025, 6, 13, 1, 0, 0, tzinfo=settings.db_zoneinfo), tick=False):
        response_before_6am = await telling_me_client.get_mobile_teller_card(user_id=user_id)
    with time_machine.travel(datetime(2025, 6, 13, 10, 0, 0, tzinfo=settings.db_zoneinfo), tick=False):
        # record는 연속 작성일을 의미한다. 6시 이전은 전날로 인식하여 time machine으로 시간 고정
        response = await telling_me_client.get_mobile_teller_card(user_id=user_id)

    code = response.json()["code"]
    message = response.json()["message"]
    data = response.json()["data"]
    badges = data["badges"]
    colors = data["colors"]
    user_info = data["userInfo"]
    level_info = data["levelInfo"]
    after_6am_record_count = data["recordCount"]
    before_6am_record_count = response_before_6am.json()["data"]["recordCount"]

    # Then user 정보 및 보유 색상 및 뱃지 조회
    assert response.status_code == status.HTTP_200_OK

    assert code == response.status_code
    assert message == "teller_card ui page"

    assert user_info["nickname"] == user_name
    assert user_info["cheeseBalance"] == cheese_amount
    assert user_info["tellerCard"]["colorCode"] == ColorCodeList.CL_DEFAULT
    assert user_info["tellerCard"]["badgeCode"] == BadgeCodeList.NEW

    assert level_info["levelDto"]["level"] == 1
    assert level_info["levelDto"]["currentExp"] == 0
    assert level_info["levelDto"]["requiredExp"] == 15
    assert after_6am_record_count == 2
    assert before_6am_record_count == 1

    assert sorted(badges, key=lambda x: x["badgeCode"]) == sorted(excepted_badges, key=lambda x: x["badgeCode"])
    assert sorted(colors, key=lambda x: x["colorCode"]) == sorted(expected_colors, key=lambda x: x["colorCode"])


async def test_get_mobile_mypage(telling_me_client: TellingMeClient, init_tortoise_connection: None) -> None:
    # Given
    user_mother = UserMother()
    badge_mother = BadgeMother()
    color_mother = ColorMother()

    user_id = await user_mother.create_user(user_name=(user_name := "telling me user"), is_premium=(is_premium := True))

    await asyncio.gather(
        user_mother.create_level_inventory(),
        badge_mother.create_badge_inventory(),
        color_mother.create_color_inventory(),
        user_mother.add_cheese(user_id=user_id, amount=(cheese_amount := 100)),
        badge_mother.create_badge(user_id=user_id, badge_code=BadgeCodeList.FIRST),
    )

    # When

    response = await telling_me_client.get_mobile_my_page(user_id=user_id)
    code = response.json()["code"]
    message = response.json()["message"]
    data = response.json()["data"]

    user_profile = data["userProfile"]
    level = data["level"]["levelDto"]

    # Then user 정보 및 보유 색상 및 뱃지 조회
    assert response.status_code == status.HTTP_200_OK

    assert code == response.status_code
    assert message == "mypage ui page"

    assert user_profile["nickname"] == user_name
    assert user_profile["cheeseBalance"] == cheese_amount
    assert user_profile["badgeCode"] == BadgeCodeList.NEW
    assert user_profile["badgeCount"] == 1
    assert user_profile["answerCount"] == 0
    assert user_profile["premium"] == is_premium
    assert not user_profile["allowNotification"]

    assert level["level"] == 1
    assert level["currentExp"] == 0
    assert level["requiredExp"] == 15
