import asyncio

from fastapi import APIRouter, status

from app.dtos.mobile.data_dto import DataDTO
from app.dtos.mobile.mypage_response import MyPageResponse
from app.dtos.mobile.teller_card_response import TellerCardResponse
from app.dtos.mobile.user_profile_with_level_dto import UserProfileWithLevelDTO
from app.dtos.user.user_info_dto import UserInfoDTO
from app.dtos.user.user_profile_dto import UserProfileDTO
from app.models.cheese_manager import CheeseManager
from app.services.answer_service import AnswerService
from app.services.badge_service import BadgeService
from app.services.color_service import ColorService
from app.services.level_service import LevelService
from app.services.teller_card_service import TellerCardService
from app.services.user_service import UserService

mobile_router = APIRouter(prefix="/mobiles", tags=["모바일 화면용 컨트롤러"])


@mobile_router.get(
    "/tellercard",
    response_model=TellerCardResponse,
    status_code=status.HTTP_200_OK,
)
async def mobile_teller_card_handler(user_id: str) -> TellerCardResponse:

    badges_task = BadgeService.get_badges_with_details_by_user_id(user_id)
    colors_task = ColorService.get_colors_with_details_by_user_id(user_id)
    level_info_task = LevelService.get_level_info_add_answer_days(user_id)
    teller_card_task = TellerCardService.get_teller_card(user_id)
    user_info_task = UserService.get_user_info(user_id)
    record_answer_task = AnswerService.get_answer_record(user_id)

    badges, colors, level_info, teller_card, user, record_count = await asyncio.gather(
        badges_task, colors_task, level_info_task, teller_card_task, user_info_task, record_answer_task
    )
    cheese_amount = await CheeseManager.get_total_cheese_amount_by_manager(cheese_manager_id=user.cheese_manager_id)
    user_info = UserInfoDTO(nickname=user.nickname, cheeseBalance=cheese_amount, tellerCard=teller_card)

    data = DataDTO(badges=badges, colors=colors, userInfo=user_info, levelInfo=level_info, recordCount=record_count)

    return TellerCardResponse(
        code=status.HTTP_200_OK,
        data=data,
        message="teller_card ui page",
    )


@mobile_router.get(
    "/mypage",
    response_model=MyPageResponse,
    status_code=status.HTTP_200_OK,
)
async def mobile_my_page_handler(user_id: str) -> MyPageResponse:

    user, answer_count, badge_count, teller_card, level = await asyncio.gather(
        UserService.get_user_profile(user_id=user_id),
        AnswerService.get_answer_count(user_id=user_id),
        BadgeService.get_badge_count(user_id=user_id),
        TellerCardService.get_teller_card(user_id=user_id),
        LevelService.get_level_info_add_answer_days(user_id),
    )

    cheese_amount = await CheeseManager.get_total_cheese_amount_by_manager(cheese_manager_id=user.cheese_manager_id)

    user_profile_data = UserProfileWithLevelDTO(
        userProfile=UserProfileDTO(
            nickname=user.nickname,
            cheeseBalance=cheese_amount,
            badgeCode=teller_card.badgeCode,
            badgeCount=badge_count,
            answerCount=answer_count,
            premium=user.is_premium,
            allowNotification=user.allow_notification,
        ),
        level=level,
    )

    return MyPageResponse(
        code=status.HTTP_200_OK,
        message="mypage ui page",
        data=user_profile_data,
    )
