import asyncio

from fastapi import APIRouter, status

from app.v2.answers.models.answer import Answer
from app.v2.badges.models.badge import Badge
from app.v2.colors.models.color import Color
from app.v2.levels.dtos.level_dto import LevelDTO

from app.v2.mobiles.dtos.mypage_response import (
    UserProfileWithLevel,
    MyPageResponseDTO,
)
from app.v2.mobiles.dtos.teller_card_response import DataDTO, TellerCardResponseDTO
from app.v2.users.dtos.user_profile_dto import UserProfileDTO
from app.v2.users.models.user import User

router = APIRouter(prefix="/mobiles", tags=["모바일 화면용 컨트롤러"])


@router.post("/main")
async def mobile_main_handler():
    pass


@router.get("/tellercard")
async def mobile_teller_card_handler():
    uuid_bytes = b"\x18\nN@b\xf8F\xbe\xb1\xeb\xe7\xe3\xdd\x91\xcd\xdf"
    # user_info -> cheese balance 처리만 하면 된다
    badges, colors, user_info, level_info = await asyncio.gather(
        Badge.get_badge_codes_by_user_id(uuid_bytes),
        Color.get_color_codes_by_user_id(uuid_bytes),
        User.get_user_info_by_user_id(uuid_bytes),
        User.get_level_info_by_user_id(uuid_bytes),
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
    uuid_bytes = b"\x18\nN@b\xf8F\xbe\xb1\xeb\xe7\xe3\xdd\x91\xcd\xdf"

    user, answer_count, (badge_count, badge_code) = await asyncio.gather(
        User.get_by_user_id(uuid_bytes=uuid_bytes),
        Answer.get_answer_count_by_user_id(uuid_bytes=uuid_bytes),
        Badge.get_badge_count_and_codes_by_user_id(uuid_bytes=uuid_bytes),
    )

    # cheese Balance, level, current_exp 필요 -> Mission 쪽
    user_profile_data = UserProfileWithLevel(
        userProfile=UserProfileDTO(
            nickname=user.nickname,
            badgeCode=badge_code,
            cheeseBalance=1000,
            badgeCount=badge_count,
            answerCount=answer_count,
            premium=user.is_premium,
        ),
        level=LevelDTO(level=user.user_level, current_exp=user.user_exp),
    )
    return MyPageResponseDTO(
        code=status.HTTP_200_OK,
        message="정상처리되었습니다",
        data=user_profile_data,
    )
