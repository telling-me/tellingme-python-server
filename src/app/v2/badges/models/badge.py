from tortoise import fields
from tortoise.models import Model

from app.v2.badges.dtos.badge_dto import BadgeCodeDTO
from common.query_executor import QueryExecutor


class Badge(Model):
    badge_id = fields.BigIntField(pk=True)  # 자동 증가하는 기본 키
    badge_code = fields.CharField(max_length=255, null=True)  # 배지 코드
    user = fields.ForeignKeyField("models.User", related_name="badges", null=True)

    class Meta:
        table = "badge"

    @classmethod
    async def get_badge_count_and_codes_by_user_id(
        cls,
        uuid_bytes: bytes,
    ) -> dict:
        hex_data = uuid_bytes.hex()
        query = f"""
            SELECT COUNT(*) as badge_count, GROUP_CONCAT(badge_code) as badge_codes
            FROM badge
            WHERE user_id = UNHEX('{hex_data}')
        """

        result = await QueryExecutor.execute_query(query, fetch_type="multiple")
        print(result)
        if result and len(result) > 0:
            return (
                result[0].get("badge_count", 0),
                result[0].get("badge_code", ""),
            )

        return {"badge_count": 0, "badge_codes": ""}

    @classmethod
    async def get_badges_with_details_by_user_id(
        cls,
        uuid_bytes: bytes,
    ) -> list:
        hex_data = uuid_bytes.hex()  # uuid_bytes를 16진수로 변환
        query = f"""
                SELECT 
                    b.badge_code,
                    bi.badge_name,
                    bi.badge_condition,
                    bi.badge_middle_name
                FROM badge b
                JOIN badge_inventory bi ON b.badge_code = bi.badge_code
                WHERE b.user_id = UNHEX('{hex_data}')
            """

        result = await QueryExecutor.execute_query(query, fetch_type="multiple")

        if result and len(result) > 0:
            return result  # 배지 정보를 딕셔너리 리스트로 반환

        return []  # 결과가 없을 경우 빈 리스트 반환

    @classmethod
    async def get_badge_codes_by_user_id(cls, uuid_bytes: bytes) -> list[BadgeCodeDTO]:
        hex_data = uuid_bytes.hex()
        query = f"SELECT badge_code FROM badge WHERE user_id = UNHEX('{hex_data}')"
        badges = await QueryExecutor.execute_query(query, fetch_type="multiple")
        return [BadgeCodeDTO(badgeCode=badge.get("badge_code")) for badge in badges]
