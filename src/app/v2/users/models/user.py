from tortoise import fields
from tortoise.models import Model

from app.v2.levels.dtos.level_dto import LevelDTO
from app.v2.teller_cards.dtos.teller_card_dto import TellerCardDTO
from app.v2.users.dtos.user_info_dto import UserInfoDTO
from common.query_executor import QueryExecutor


class User(Model):
    user_id = fields.CharField(max_length=54, pk=True)
    allow_notification = fields.BooleanField(null=True)
    birth_date = fields.CharField(max_length=8, null=True)
    created_time = fields.DatetimeField(auto_now_add=True)
    gender = fields.CharField(max_length=16, null=True)
    job = fields.IntField()
    mbti = fields.CharField(max_length=8, null=True)
    nickname = fields.CharField(max_length=16)
    purpose = fields.CharField(max_length=16)
    push_token = fields.CharField(max_length=255, null=True)
    social_id = fields.CharField(max_length=255)
    social_login_type = fields.CharField(max_length=16)
    user_status = fields.BooleanField()
    withdraw_period = fields.DatetimeField(null=True)
    refresh_token = fields.ForeignKeyField(
        "models.RefreshToken",
        related_name="users",
        db_column="refresh_token_id",
        null=True,
    )
    is_premium = fields.BooleanField()
    profile_url = fields.CharField(
        max_length=255,
        default="https://miro.medium.com/v2/resize:fit:1400/format:webp/1*dh7Xy5tFvRj7n2wf1UweAw.png",
    )
    premium_started_at = fields.DatetimeField(null=True)
    user_exp = fields.IntField(null=True)
    user_level = fields.IntField(null=True)
    cheese_manager = fields.ForeignKeyField(
        "models.CheeseManager",
        related_name="users",
        db_column="cheese_manager_id",
        null=True,
    )
    teller_card = fields.ForeignKeyField(
        "models.TellerCard",
        related_name="users",
        db_column="teller_card_id",
        null=True,
    )

    class Meta:
        table = "user"

    @classmethod
    async def get_by_user_id(cls, uuid_bytes: bytes) -> "User":
        hex_data = uuid_bytes.hex()
        print(hex_data)
        users = await cls.raw(
            f"SELECT * FROM user WHERE user_id = 0x{hex_data} LIMIT 1"
        )
        if users:
            return users[0]  # 첫 번째 결과 반환
        else:
            return None

    @classmethod
    async def get_user_info_by_user_id(cls, uuid_bytes: bytes) -> UserInfoDTO:
        hex_data = uuid_bytes.hex()
        query = f"""
            SELECT 
                u.nickname,
                u.cheese_balance,
                tc.activate_badge_code AS badgeCode,
                bi.badge_name AS badgeName,
                bi.badge_middle_name AS badgeMiddleName,
                tc.activate_color_code AS colorCode
            FROM user u
            JOIN teller_card tc ON u.teller_card_id = tc.teller_card_id
            JOIN badge_inventory bi ON tc.activate_badge_code = bi.badge_code
            WHERE u.user_id = UNHEX('{hex_data}')
        """
        result = await QueryExecutor.execute_query(query, fetch_type="single")
        if result:
            user = result[0]
            teller_card = TellerCardDTO(
                badgeCode=user.get("badgeCode"),
                badgeName=user.get("badgeName"),
                badgeMiddleName=user.get("badgeMiddleName"),
                colorCode=user.get("colorCode"),
            )
            return UserInfoDTO(
                nickname=user.get("nickname"),
                cheeseBalance=user.get("cheese_balance"),
                tellerCard=teller_card,
            )
        return None

    @classmethod
    async def get_level_info_by_user_id(cls, uuid_bytes: bytes) -> LevelDTO:
        hex_data = uuid_bytes.hex()
        query = f"SELECT user_level AS level, user_exp AS current_exp FROM user WHERE user_id = UNHEX('{hex_data}')"
        result = await QueryExecutor.execute_query(query, fetch_type="multiple")
        if result:
            level_data = result[0]
            return LevelDTO(
                level=level_data.get("level"), current_exp=level_data.get("current_exp")
            )
        return None
