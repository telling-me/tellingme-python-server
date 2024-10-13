from tortoise import fields
from tortoise.models import Model
from uuid import UUID

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
