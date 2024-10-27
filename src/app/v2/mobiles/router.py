import asyncio

from fastapi import APIRouter, status, HTTPException

from app.v2.answers.models.answer import Answer

from app.v2.badges.models.badge import Badge
from app.v2.badges.services.badge_service import BadgeService
from app.v2.cheese_managers.models.cheese_manager import CheeseManager
from app.v2.cheese_managers.services.cheese_service import CheeseService

from app.v2.colors.services.color_service import ColorService
from app.v2.levels.dtos.level_dto import LevelDTO
from app.v2.levels.models.level import Level
from app.v2.levels.services.level_service import LevelService

from app.v2.mobiles.dtos.mypage_response import (
    UserProfileWithLevel,
    MyPageResponseDTO,
)
from app.v2.mobiles.dtos.teller_card_response import DataDTO, TellerCardResponseDTO

from app.v2.teller_cards.services.teller_card_service import TellerCardService
from app.v2.users.dtos.user_info_dto import UserInfoDTO
from app.v2.users.dtos.user_profile_dto import UserProfileDTO
from app.v2.users.models.user import User
from app.v2.users.services.user_service import UserService

router = APIRouter(prefix="/mobiles", tags=["모바일 화면용 컨트롤러"])


@router.post("/main")
async def mobile_main_handler():
    pass


@router.get(
    "/tellercard",
    response_model=TellerCardResponseDTO,
    status_code=status.HTTP_200_OK,
)
async def mobile_teller_card_handler():
    user_id = "180a4e40-62f8-46be-b1eb-e7e3dd91cddf"

    try:
        badges_task = BadgeService.get_badges(user_id)
        colors_task = ColorService.get_colors(user_id)
        level_info_task = LevelService.get_level_info(user_id)  # LevelService 추가
        teller_card_task = TellerCardService.get_teller_card(user_id)
        user_info_task = UserService.get_user_info(user_id)

        badges, colors, level_info, teller_card, user_raw = await asyncio.gather(
            badges_task, colors_task, level_info_task, teller_card_task, user_info_task
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="내부 서버 오류")

    cheese_amount = await CheeseService.get_cheese_balance(
        user_raw["cheese_manager_id"]
    )

    user_info = UserInfoDTO.builder(
        user_raw, cheeseBalance=cheese_amount, tellerCard=teller_card
    )

    data = DataDTO(badges=badges, colors=colors, userInfo=user_info, level=level_info)

    return TellerCardResponseDTO(
        code=status.HTTP_200_OK,
        data=data,
        message="teller_card ui page",
    )


@router.get(
    "/mypage",
    response_model=MyPageResponseDTO,
    status_code=status.HTTP_200_OK,
)
async def mobile_my_page_handler():
    user_id = "180a4e40-62f8-46be-b1eb-e7e3dd91cddf"

    user, answer_count, (badge_count, badge_code), level = await asyncio.gather(
        User.get_user_profile_by_user_id(user_id=user_id),
        Answer.get_answer_count_by_user_id(user_id=user_id),
        Badge.get_badge_count_and_codes_by_user_id(user_id=user_id),
        Level.get_level_info_by_user_id(user_id=user_id),
    )

    cheese_amount = await CheeseManager.get_total_cheese_amount_by_manager()

    user_profile_data = UserProfileWithLevel(
        userProfile=UserProfileDTO(
            nickname=user["nickname"],
            badgeCode=badge_code,
            cheeseBalance=cheese_amount,
            badgeCount=badge_count,
            answerCount=answer_count["answer_count"],
            premium=bool(user["is_premium"]),
        ),
        level=LevelDTO(
            level=level.get("level_level"), current_exp=level.get("level_exp")
        ),
    )
    return MyPageResponseDTO(
        code=status.HTTP_200_OK,
        message="정상처리되었습니다",
        data=user_profile_data,
    )
