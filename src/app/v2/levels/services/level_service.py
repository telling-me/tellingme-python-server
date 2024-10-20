import asyncio

from app.v2.levels.dtos.level_dto import LevelDTO
from app.v2.levels.models.level import Level


class LevelService:
    @classmethod
    async def get_level_info(cls, user_id: str) -> LevelDTO:
        # 레벨 정보를 조회하는 로직
        level_info_raw = await Level.get_level_info_by_user_id(user_id=user_id)
        return LevelDTO.builder(
            level=level_info_raw.get("level_level"),
            current_exp=level_info_raw.get("level_exp"),
        )

    @classmethod
    async def level_up(cls, user_id: str) -> dict:
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

            return {
                "status": "success",
                "message": "레벨업 성공",
                "new_level": new_level,
                "remaining_exp": new_exp,
            }

        return {
            "status": "failure",
            "message": "레벨업에 필요한 경험치가 부족합니다",
            "current_level": level,
            "current_exp": current_exp,
            "required_exp": required_exp,
        }
