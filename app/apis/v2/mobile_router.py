import asyncio

from fastapi import APIRouter, status

from app.dtos.mobile.mypage_response import MyPageResponseDTO, UserProfileWithLevel
from app.dtos.mobile.teller_card_response import DataDTO, TellerCardResponseDTO
from app.dtos.user.user_info_dto import UserInfoDTO
from app.dtos.user.user_profile_dto import UserProfileDTO
from app.services.answer_service import AnswerService
from app.services.badge_service import BadgeService
from app.services.cheese_service import CheeseService
from app.services.color_service import ColorService
from app.services.level_service import LevelService
from app.services.teller_card_service import TellerCardService
from app.services.user_service import UserService

mobile_router = APIRouter(prefix="/mobiles", tags=["모바일 화면용 컨트롤러"])


@mobile_router.get(
    "/tellercard",
    response_model=TellerCardResponseDTO,
    status_code=status.HTTP_200_OK,
)
async def mobile_teller_card_handler(user_id: str) -> TellerCardResponseDTO:

    badges_task = BadgeService.get_badges_with_details_by_user_id(user_id)
    colors_task = ColorService.get_colors_with_details_by_user_id(user_id)
    level_info_task = LevelService.get_level_info_add_answer_days(user_id)
    teller_card_task = TellerCardService.get_teller_card(user_id)
    user_info_task = UserService.get_user_info(user_id)
    record_answer_task = AnswerService.get_answer_record(user_id=user_id)

    badges, colors, level_info, teller_card, user_raw, record_count = await asyncio.gather(
        badges_task, colors_task, level_info_task, teller_card_task, user_info_task, record_answer_task
    )

    cheese_amount = await CheeseService.get_cheese_balance(user_raw.cheese_manager_id)

    user_info = UserInfoDTO(nickname=user_raw.nickname, cheeseBalance=cheese_amount, tellerCard=teller_card)

    data = DataDTO.builder(
        badges=badges, colors=colors, userInfo=user_info, levelInfo=level_info, recordCount=record_count
    )

    return TellerCardResponseDTO(
        code=status.HTTP_200_OK,
        data=data,
        message="teller_card ui page",
    )


@mobile_router.get(
    "/mypage",
    response_model=MyPageResponseDTO,
    status_code=status.HTTP_200_OK,
)
async def mobile_my_page_handler(user_id: str) -> MyPageResponseDTO:

    user, answer_count, badge_count, teller_card, level = await asyncio.gather(
        UserService.get_user_profile(user_id=user_id),
        AnswerService.get_answer_count(user_id=user_id),
        BadgeService.get_badge_count(user_id=user_id),
        TellerCardService.get_teller_card(user_id=user_id),
        LevelService.get_level_info_add_answer_days(user_id),
    )

    cheese_amount = await CheeseService.get_cheese_balance(cheese_manager_id=user.cheese_manager_id)  # type: ignore

    user_profile_data = UserProfileWithLevel.builder(
        userProfile=UserProfileDTO.builder(
            nickname=user.nickname,  # type: ignore
            cheeseBalance=cheese_amount,
            badgeCode=teller_card.badgeCode,
            badgeCount=badge_count,
            answerCount=answer_count,
            premium=user.is_premium,  # type: ignore
            allow_notification=user.allow_notification,  # type: ignore
        ),
        level=level,
    )

    return MyPageResponseDTO(
        code=status.HTTP_200_OK,
        message="정상처리되었습니다",
        data=user_profile_data,
    )
