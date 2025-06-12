from app.dtos.user.user_data import UserData
from app.dtos.user.user_dto import UserProfileData
from app.models.cheese_manager import CheeseManager
from app.models.color import Color
from app.models.emotion import Emotion
from app.models.level import Level
from app.models.mission import UserMission
from app.models.teller_card import TellerCard
from app.models.user import User


class UserService:

    @staticmethod
    async def create_user(is_premium: bool = False) -> str:
        cheese_manager = await CheeseManager.create_cheese_manager()
        teller_card = await TellerCard.create(activate_badge_code="BG_NEW", activate_color_code="CL_DEFAULT")
        level = await Level.create(user_exp=0, user_level=1)
        user_id = await User.create_user(
            social_id="kakao_456",
            social_login_type="kakao",
            nickname="test_user",
            purpose="test",
            job=1,
            cheese_manager_id=cheese_manager.cheese_manager_id,
            teller_card_id=teller_card.teller_card_id,
            level_id=level.level_id,
            is_premium=is_premium,
        )
        await Color.create_default_by_user_id(user_id=user_id)
        await Emotion.create_default_emotions_by_user_id(user_id=user_id)
        await UserMission.create_default_missions_by_user_id(user_id=user_id)
        return user_id

    @staticmethod
    async def get_user_info(user_id: str) -> UserData:
        return await User.get_user_info_by_user_id(user_id=user_id)

    @classmethod
    async def get_user_profile(cls, user_id: str) -> UserProfileData:
        return await User.get_user_profile_by_user_id(user_id=user_id)

    @staticmethod
    async def set_is_premium(user_id: str, is_premium: bool) -> None:
        await User.set_is_premium(user_id=user_id, is_premium=is_premium)
