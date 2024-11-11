import asyncio

from app.v2.levels.dtos.level_dto import LevelDTO
from app.v2.levels.models.level import Level


class LevelService:
    @classmethod
    async def get_level_info(cls, user_id: str) -> LevelDTO:
        # 레벨 정보를 조회하는 로직
        level_info_raw = await Level.get_level_info_by_user_id(user_id=user_id)
        required_exp_raw = await Level.get_required_exp_by_user_id(user_id=user_id)
        return LevelDTO.builder(
            level=level_info_raw.get("level_level"),
            current_exp=level_info_raw.get("level_exp"),
            required_exp=required_exp_raw.get("required_exp"),
        )

    @classmethod
    async def level_up(cls, user_id: str) -> int:
        """
        유저가 레벨업 가능한지 확인 후, 레벨업 처리
        """
        level_dto, required_exp_raw = await asyncio.gather(
            cls.get_level_info(user_id=user_id),
            Level.get_required_exp_by_user_id(user_id=user_id),
        )

        level = level_dto.level
        current_exp = level_dto.current_exp
        required_exp = required_exp_raw["required_exp"]

        if current_exp >= required_exp:
            new_exp = current_exp - required_exp
            new_level = level + 1

            await Level.update_level_and_exp(
                user_id=user_id, new_level=new_level, new_exp=new_exp
            )
            return 1
        return 0

    @classmethod
    async def add_exp(cls, user_id: str, exp: int) -> None:
        level_dto = await cls.get_level_info(user_id=user_id)

        current_exp = level_dto.current_exp
        new_exp = current_exp + exp

        await Level.update_level_and_exp(
            user_id=user_id, new_level=level_dto.level, new_exp=new_exp
        )
