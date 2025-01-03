from typing import Optional

from app.v2.badges.models.badge import BadgeInventory
from app.v2.notices.models.notice import Notice


class NoticeService:

    @classmethod
    async def create_notice(
        cls,
        user_id: str,
        title: str,
        reward_type: str,
        content: str,
        badge_code: Optional[str] = None,
    ) -> None:
        return await Notice.create_notice(
            title=title,
            content=content,
            user_id=user_id,
            reward_type=reward_type,
            is_internal=True,
            is_read=False,
            badge_code=badge_code,
        )

    @classmethod
    async def create_reward_notice(
        cls,
        user_id: str,
        reward_type: str,
        total_cheese: int = 0,
        total_exp: int = 0,
        badge_full_name: Optional[str] = None,
        badge_code: Optional[str] = None,
        level_up: Optional[bool] = False,
        nickname: Optional[str] = None,
        new_level: Optional[int] = None,
    ) -> None:
        if not badge_code and not level_up and total_cheese == 0 and total_exp == 0:
            return

        # 1. 제목 생성
        title = cls.create_title(
            badge_full_name=badge_full_name,
            level_up=level_up,
            nickname=nickname,
            new_level=new_level,
        )

        # 2. 메시지 생성
        content = cls.create_reward_message(
            total_cheese=total_cheese,
            total_exp=total_exp,
            badge_full_name=badge_full_name,
            level_up=level_up,
        )

        badge_code = badge_code if badge_code else None

        # 3. 알림 생성
        await cls.create_notice(
            user_id=user_id, title=title, content=content, reward_type=reward_type, badge_code=badge_code
        )

    @classmethod
    def create_title(
        cls,
        badge_full_name: Optional[str] = None,
        level_up: Optional[bool] = False,
        nickname: Optional[str] = None,
        new_level: Optional[int] = None,
    ) -> str:
        if level_up and nickname and new_level is not None:
            return f"{nickname} LV{new_level}로 레벨업!"
        if badge_full_name:
            return badge_full_name
        return "보상을 받았어요!"

    @classmethod
    def create_reward_message(
        cls, total_cheese: int, total_exp: int, badge_full_name: Optional[str] = None, level_up: Optional[bool] = False
    ) -> str:
        if level_up:
            return f"선물로 치즈 {total_cheese}개를 드릴게요!" if total_cheese > 0 else "레벨업을 축하드립니다!"

        if badge_full_name:
            return f"선물로 치즈 {total_cheese}개를 드릴게요!" if total_cheese > 0 else "뱃지 획득을 축하드립니다!"

        if total_cheese > 0 and total_exp > 0:
            return f"치즈 {total_cheese}개와 경험치 {total_exp}P를 받았어요!"
        elif total_cheese > 0:
            return f"치즈 {total_cheese}개를 받았어요!"
        elif total_exp > 0:
            return f"경험치 {total_exp}P를 받았어요!"
        return "보상을 받지 못했어요!"
