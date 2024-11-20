import asyncio

from fastapi import APIRouter, HTTPException, status

from app.v2.answers.services.answer_service import AnswerService
from app.v2.badges.services.badge_service import BadgeService
from app.v2.cheese_managers.models.cheese_manager import CheeseManager
from app.v2.cheese_managers.services.cheese_service import CheeseService
from app.v2.colors.services.color_service import ColorService
from app.v2.levels.services.level_service import LevelService
from app.v2.mobiles.dtos.mypage_response import MyPageResponseDTO, UserProfileWithLevel
from app.v2.mobiles.dtos.teller_card_response import DataDTO, TellerCardResponseDTO
from app.v2.teller_cards.services.teller_card_service import TellerCardService
from app.v2.users.dtos.user_info_dto import UserInfoDTO
from app.v2.users.dtos.user_profile_dto import UserProfileDTO
from app.v2.users.services.user_service import UserService

router = APIRouter(prefix="/mobiles", tags=["모바일 화면용 컨트롤러"])


@router.post("/main")
async def mobile_main_handler() -> None:
    pass


@router.get(
    "/tellercard",
    response_model=TellerCardResponseDTO,
    status_code=status.HTTP_200_OK,
)
async def mobile_teller_card_handler(user_id: str) -> TellerCardResponseDTO:
    try:
        badges_task = BadgeService.get_badges_with_details_by_user_id(user_id)
        colors_task = ColorService.get_colors(user_id)
        level_info_task = LevelService.get_level_info_add_answer_days(user_id)
        teller_card_task = TellerCardService.get_teller_card(user_id)
        user_info_task = UserService.get_user_info(user_id)

        badges, colors, level_info, teller_card, user_raw = await asyncio.gather(
            badges_task, colors_task, level_info_task, teller_card_task, user_info_task
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    cheese_amount = await CheeseService.get_cheese_balance(user_raw["cheese_manager_id"])

    user_info = UserInfoDTO.builder(user_raw, cheeseBalance=cheese_amount, tellerCard=teller_card)

    data = DataDTO.builder(badges=badges, colors=colors, userInfo=user_info, levelInfo=level_info)

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
async def mobile_my_page_handler(user_id: str) -> MyPageResponseDTO:

    user, answer_count, badge_count, teller_card, level = await asyncio.gather(
        UserService.get_user_profile(user_id=user_id),
        AnswerService.get_answer_count(user_id=user_id),
        BadgeService.get_badge_count(user_id=user_id),
        TellerCardService.get_teller_card(user_id=user_id),
        LevelService.get_level_info_add_answer_days(user_id),
    )

    cheese_amount = await CheeseManager.get_total_cheese_amount_by_manager(cheese_manager_id=user["cheese_manager_id"])

    user_profile_data = UserProfileWithLevel.builder(
        userProfile=UserProfileDTO.builder(
            nickname=user["nickname"],
            cheeseBalance=cheese_amount,
            badgeCode=teller_card.badgeCode,
            badgeCount=badge_count,
            answerCount=answer_count,
            premium=bool(user["is_premium"]),
        ),
        level=level,
    )

    return MyPageResponseDTO(
        code=status.HTTP_200_OK,
        message="정상처리되었습니다",
        data=user_profile_data,
    )
