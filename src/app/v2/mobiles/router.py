import asyncio

from fastapi import APIRouter, status

from app.v2.answers.models.answer import Answer
from app.v2.badges.models.badge import Badge
from app.v2.levels.dtos.level_dto import LevelDto
from app.v2.mobiles.dtos.responses import (
    UserProfileWithLevelResponseDTO,
    UserProfileWithLevel,
)
from app.v2.users.dtos.user_profile_dto import UserProfileDto
from app.v2.users.models.user import User

router = APIRouter(prefix="/mobiles", tags=["모바일 화면용 컨트롤러"])


@router.post("/main")
async def mobile_main_handler():
    pass


@router.get("/tellercard")
async def mobile_teller_card_handler():
    pass


@router.get(
    "/mypage",
    response_model=UserProfileWithLevelResponseDTO,
    status_code=status.HTTP_200_OK,
    deprecated="마이페이지 UI용 API입니다",
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
        userProfile=UserProfileDto(
            nickname=user.nickname,
            badgeCode=badge_code,
            cheeseBalance=1000,
            badgeCount=badge_count,
            answerCount=answer_count,
            premium=user.is_premium,
        ),
        level=LevelDto(level=1, current_exp=10),
    )
    return UserProfileWithLevelResponseDTO(
        code=status.HTTP_200_OK,
        message="정상처리되었습니다",
        data=user_profile_data,
    )
