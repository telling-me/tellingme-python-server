from app.services.user_service import UserService


class UserMother:

    @staticmethod
    async def create_user() -> str:
        user_service = UserService()
        new_user_id = await user_service.create_user()
        return new_user_id
