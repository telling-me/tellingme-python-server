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
        total_cheese: int,
        total_exp: int,
    ) -> Notice:
        if total_cheese == 0 and total_exp == 0:
            return

        return await cls.create_notice(
            user_id=user_id,
            title="보상을 받았어요!",
            content=cls.create_reward_message(total_cheese=total_cheese, total_exp=total_exp),
            reward_type=reward_type,
        )

    @classmethod
    def create_reward_message(cls, total_cheese: int, total_exp: int) -> str:
        if total_cheese > 0 and total_exp > 0:
            return f"치즈 {total_cheese}개와 경험치 {total_exp}P를 받았어요!"
        elif total_cheese > 0:
            return f"치즈 {total_cheese}개를 받았어요!"
        elif total_exp > 0:
            return f"경험치 {total_exp}P를 받았어요!"
        else:
            return "보상을 받지 못했어요!"
