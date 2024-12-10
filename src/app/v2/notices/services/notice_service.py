from app.v2.notices.models.notice import Notice


class NoticeService:

    @classmethod
    async def create_notice(
        cls,
        user_id: str,
        title: str,
        reward_type: str,
        content: str,
    ) -> Notice:
        return await Notice.create_notice(
            title=title,
            content=content,
            user_id=user_id,
            reward_type=reward_type,
            is_internal=True,
            is_read=False,
        )

    @classmethod
    async def create_reward_notice(
        cls,
        user_id: str,
        reward_type: str,
        total_cheese: int = 0,
        total_exp: int = 0,
        badge_info: str = None,
    ) -> Notice:
        if not badge_info and total_cheese == 0 and total_exp == 0:
            return

        # 1. 제목 생성
        title = cls.create_title(badge_info)

        # 2. 메시지 생성
        content = cls.create_reward_message(total_cheese, total_exp, badge_info)

        # 3. 알림 생성
        return await cls.create_notice(
            user_id=user_id,
            title=title,
            content=content,
            reward_type=reward_type,
        )

    @classmethod
    def create_title(cls, badge: str = None) -> str:
        if badge:
            return badge
        return "보상을 받았어요!"

    @classmethod
    def create_reward_message(cls, total_cheese: int, total_exp: int, badge: str = None) -> str:
        if badge:
            return f"선물로 치즈 {total_cheese}개를 드릴게요!" if total_cheese > 0 else "뱃지 획득을 축하드립니다!"

        if total_cheese > 0 and total_exp > 0:
            return f"치즈 {total_cheese}개와 경험치 {total_exp}P를 받았어요!"
        elif total_cheese > 0:
            return f"치즈 {total_cheese}개를 받았어요!"
        elif total_exp > 0:
            return f"경험치 {total_exp}P를 받았어요!"
        return "보상을 받지 못했어요!"
