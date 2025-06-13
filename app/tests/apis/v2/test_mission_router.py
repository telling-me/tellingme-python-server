import asyncio
from datetime import datetime

import time_machine

from app.common.constants.badge_code_list import BadgeCodeList
from app.common.constants.color_code_list import ColorCodeList
from app.core.configs import settings
from app.tests.mothers.answer_mother import AnswerMother
from app.tests.mothers.badge_mother import BadgeMother
from app.tests.mothers.color_mother import ColorMother
from app.tests.mothers.emotion_mother import EmotionMother
from app.tests.mothers.item_mother import ItemMother
from app.tests.mothers.mission_mother import MissionMother
from app.tests.mothers.user_mother import UserMother
from app.tests.telling_me_client import TellingMeClient


async def test_mission_check_first_post(telling_me_client: TellingMeClient, init_tortoise_connection: None) -> None:
    # Given
    user_mother = UserMother()
    answer_mother = AnswerMother()
    color_mother = ColorMother()
    badge_mother = BadgeMother()
    emotion_mother = EmotionMother()
    item_mother = ItemMother()
    mission_mother = MissionMother()

    user_id = await user_mother.create_user(user_name="telling me user")

    await asyncio.gather(
        user_mother.create_level_inventory(),
        badge_mother.create_badge_inventory(),
        color_mother.create_color_inventory(),
        emotion_mother.create_emotion_inventory(),
        mission_mother.create_mission_inventory(),
        item_mother.create_item_inventory_and_reward_inventory(),
        user_mother.add_cheese(user_id=user_id, amount=0),
        answer_mother.create_answer(user_id=user_id, content="-", date="2025-06-13"),
    )

    # When
    with time_machine.travel(datetime(2025, 6, 13, 10, 0, 0, tzinfo=settings.db_zoneinfo), tick=False):
        await telling_me_client.check_mission(user_id=user_id)

    response = await telling_me_client.get_mobile_teller_card(user_id=user_id)
    badge_codes = [badge["badgeCode"] for badge in response.json()["data"]["badges"]]
    level_info = response.json()["data"]["levelInfo"]["levelDto"]

    # Then 첫 글 작성 시 Badge code First + 경험치 11 ( 첫 글 작성 10 + 기본 1 )
    assert BadgeCodeList.FIRST in badge_codes
    assert level_info["currentExp"] == 11


async def test_mission_check_long_post(telling_me_client: TellingMeClient, init_tortoise_connection: None) -> None:
    # Given
    user_mother = UserMother()
    answer_mother = AnswerMother()
    color_mother = ColorMother()
    badge_mother = BadgeMother()
    emotion_mother = EmotionMother()
    item_mother = ItemMother()
    mission_mother = MissionMother()

    user_id = await user_mother.create_user(user_name="telling me user")

    await asyncio.gather(
        user_mother.create_level_inventory(),
        badge_mother.create_badge_inventory(),
        color_mother.create_color_inventory(),
        emotion_mother.create_emotion_inventory(),
        mission_mother.create_mission_inventory(),
        item_mother.create_item_inventory_and_reward_inventory(),
        user_mother.add_cheese(user_id=user_id, amount=0),
        answer_mother.create_answer(
            user_id=user_id, content="이것은 텔러가 작성한 280자 이상의 긴 답변입니다. " * 10, date="2025-06-13"
        ),
    )

    # When
    with time_machine.travel(datetime(2025, 6, 13, 10, 0, 0, tzinfo=settings.db_zoneinfo), tick=False):
        await telling_me_client.check_mission(user_id=user_id)

    response = await telling_me_client.get_mobile_teller_card(user_id=user_id)
    badge_codes = [badge["badgeCode"] for badge in response.json()["data"]["badges"]]

    # Then 280자 이상 글 작성 시 뱃지 지급
    assert BadgeCodeList.MUCH_001 in badge_codes


async def test_mission_check_consecutive_7_days(
    telling_me_client: TellingMeClient, init_tortoise_connection: None
) -> None:
    # Given
    user_mother = UserMother()
    answer_mother = AnswerMother()
    color_mother = ColorMother()
    badge_mother = BadgeMother()
    emotion_mother = EmotionMother()
    item_mother = ItemMother()
    mission_mother = MissionMother()

    user_id = await user_mother.create_user(user_name="telling me user")

    await asyncio.gather(
        user_mother.create_level_inventory(),
        badge_mother.create_badge_inventory(),
        color_mother.create_color_inventory(),
        emotion_mother.create_emotion_inventory(),
        mission_mother.create_mission_inventory(),
        item_mother.create_item_inventory_and_reward_inventory(),
        user_mother.add_cheese(user_id=user_id, amount=0),
        answer_mother.create_answer(user_id=user_id, content="-", date="2025-06-07"),
        answer_mother.create_answer(user_id=user_id, content="-", date="2025-06-08"),
        answer_mother.create_answer(user_id=user_id, content="-", date="2025-06-09"),
        answer_mother.create_answer(user_id=user_id, content="-", date="2025-06-10"),
        answer_mother.create_answer(user_id=user_id, content="-", date="2025-06-11"),
        answer_mother.create_answer(user_id=user_id, content="-", date="2025-06-12"),
        answer_mother.create_answer(user_id=user_id, content="-", date="2025-06-13"),
    )

    # When
    with time_machine.travel(datetime(2025, 6, 13, 10, 0, 0, tzinfo=settings.db_zoneinfo), tick=False):
        await telling_me_client.check_mission(user_id=user_id)

    response = await telling_me_client.get_mobile_teller_card(user_id=user_id)
    badge_codes = [badge["badgeCode"] for badge in response.json()["data"]["badges"]]

    # Then 연속 7일 글 작성 시 Badge code AGAIN
    assert BadgeCodeList.AGAIN_001 in badge_codes


async def test_mission_check_cheese_50(telling_me_client: TellingMeClient, init_tortoise_connection: None) -> None:
    # Given
    user_mother = UserMother()
    color_mother = ColorMother()
    badge_mother = BadgeMother()
    emotion_mother = EmotionMother()
    item_mother = ItemMother()
    mission_mother = MissionMother()

    user_id = await user_mother.create_user(user_name="telling me user")

    await asyncio.gather(
        user_mother.create_level_inventory(),
        badge_mother.create_badge_inventory(),
        color_mother.create_color_inventory(),
        emotion_mother.create_emotion_inventory(),
        mission_mother.create_mission_inventory(),
        item_mother.create_item_inventory_and_reward_inventory(),
        user_mother.add_cheese(user_id=user_id, amount=50),
    )

    # When
    with time_machine.travel(datetime(2025, 6, 13, 10, 0, 0, tzinfo=settings.db_zoneinfo), tick=False):
        await telling_me_client.check_mission(user_id=user_id)

    response = await telling_me_client.get_mobile_teller_card(user_id=user_id)
    badge_codes = [badge["badgeCode"] for badge in response.json()["data"]["badges"]]

    # Then 총 치즈 누적량 50 이상
    assert BadgeCodeList.SAVE_001 in badge_codes


async def test_mission_christmas(telling_me_client: TellingMeClient, init_tortoise_connection: None) -> None:
    # Given
    user_mother = UserMother()
    color_mother = ColorMother()
    badge_mother = BadgeMother()
    emotion_mother = EmotionMother()
    item_mother = ItemMother()
    mission_mother = MissionMother()

    with time_machine.travel(datetime(2024, 12, 25, 10, 0, 0, tzinfo=settings.db_zoneinfo), tick=False):
        user_id = await user_mother.create_user(user_name="telling me user")

    await asyncio.gather(
        user_mother.create_level_inventory(),
        badge_mother.create_badge_inventory(),
        color_mother.create_color_inventory(),
        emotion_mother.create_emotion_inventory(),
        mission_mother.create_mission_inventory(),
        item_mother.create_item_inventory_and_reward_inventory(),
        user_mother.add_cheese(user_id=user_id, amount=50),
    )

    # When
    with time_machine.travel(datetime(2024, 12, 25, 10, 0, 0, tzinfo=settings.db_zoneinfo), tick=False):
        await telling_me_client.check_mission(user_id=user_id)

    response = await telling_me_client.get_mobile_teller_card(user_id=user_id)
    badge_codes = [badge["badgeCode"] for badge in response.json()["data"]["badges"]]
    color_codes = [badge["colorCode"] for badge in response.json()["data"]["colors"]]

    # Then 2024년 크리스마스 기간에 접속 했을 시 뱃지 및 색상 지급
    assert BadgeCodeList.CHRISTMAS_2024 in badge_codes
    assert ColorCodeList.CL_RED_001 in color_codes


async def test_mission_post_2_5(telling_me_client: TellingMeClient, init_tortoise_connection: None) -> None:
    # Given
    user_mother = UserMother()
    answer_mother = AnswerMother()
    color_mother = ColorMother()
    badge_mother = BadgeMother()
    emotion_mother = EmotionMother()
    item_mother = ItemMother()
    mission_mother = MissionMother()

    user_id = await user_mother.create_user(user_name="telling me user")

    await asyncio.gather(
        user_mother.create_level_inventory(),
        badge_mother.create_badge_inventory(),
        color_mother.create_color_inventory(),
        emotion_mother.create_emotion_inventory(),
        mission_mother.create_mission_inventory(),
        item_mother.create_item_inventory_and_reward_inventory(),
        user_mother.add_cheese(user_id=user_id, amount=50),
    )

    # When
    with time_machine.travel(datetime(2025, 6, 11, 10, 0, 0, tzinfo=settings.db_zoneinfo), tick=False):
        await answer_mother.create_answer(user_id=user_id, content="-", date="2025-06-11")
        await telling_me_client.check_mission(user_id=user_id)
        await mission_mother.reset_mission()

    with time_machine.travel(datetime(2025, 6, 12, 10, 0, 0, tzinfo=settings.db_zoneinfo), tick=False):
        await answer_mother.create_answer(user_id=user_id, content="-", date="2025-06-12")
        await telling_me_client.check_mission(user_id=user_id)
        await mission_mother.reset_mission()

    with time_machine.travel(datetime(2025, 6, 13, 10, 0, 0, tzinfo=settings.db_zoneinfo), tick=False):
        await answer_mother.create_answer(user_id=user_id, content="-", date="2025-06-13")
        await telling_me_client.check_mission(user_id=user_id)
        await mission_mother.reset_mission()

    response = await telling_me_client.get_mobile_teller_card(user_id=user_id)
    level_info = response.json()["data"]["levelInfo"]["levelDto"]

    # Then 첫 날 경험치 11 ( 첫 글 작성 10 + 기본 1 ) + 둘쨰날 경험치 7 ( 2~5 작성 시 5pt + 연속 작성 2pt )  + 셋째날 경험치 8 ( 2~5 작성 시 5pt + 연속 작성 3pt )
    assert level_info["level"] == 2
    assert level_info["currentExp"] == 11


async def test_mission_level_up(telling_me_client: TellingMeClient, init_tortoise_connection: None) -> None:
    # Given
    user_mother = UserMother()
    answer_mother = AnswerMother()
    color_mother = ColorMother()
    badge_mother = BadgeMother()
    emotion_mother = EmotionMother()
    item_mother = ItemMother()
    mission_mother = MissionMother()

    user_id = await user_mother.create_user(user_name="telling me user")

    await asyncio.gather(
        user_mother.create_level_inventory(),
        badge_mother.create_badge_inventory(),
        color_mother.create_color_inventory(),
        emotion_mother.create_emotion_inventory(),
        mission_mother.create_mission_inventory(),
        item_mother.create_item_inventory_and_reward_inventory(),
        user_mother.add_cheese(user_id=user_id, amount=0),
    )

    # When
    with time_machine.travel(datetime(2025, 6, 12, 10, 0, 0, tzinfo=settings.db_zoneinfo), tick=False):
        await answer_mother.create_answer(user_id=user_id, content="-", date="2025-06-12")
        await telling_me_client.check_mission(user_id=user_id)
        await mission_mother.reset_mission()

    with time_machine.travel(datetime(2025, 6, 13, 10, 0, 0, tzinfo=settings.db_zoneinfo), tick=False):
        await answer_mother.create_answer(user_id=user_id, content="-", date="2025-06-13")
        await telling_me_client.check_mission(user_id=user_id)
        await mission_mother.reset_mission()

    response = await telling_me_client.get_mobile_teller_card(user_id=user_id)
    cheese_balance = response.json()["data"]["userInfo"]["cheeseBalance"]
    level_info = response.json()["data"]["levelInfo"]["levelDto"]

    # Then 첫 날 경험치 11 ( 첫 글 작성 10 + 기본 1 ) + 둘쨰날 경험치 7 ( 2~5 작성 시 5pt + 연속 작성 2pt )
    assert level_info["level"] == 2
    assert level_info["currentExp"] == 3
    assert cheese_balance == 1 + 2  # 첫 글 보상 치즈 10 + 레벨업 보상 치즈 1 + 연속 작성 2일 보상 치즈 2개
