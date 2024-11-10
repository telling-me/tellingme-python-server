from tortoise import fields
from tortoise.models import Model

from app.v2.teller_cards.querys.teller_card_query import (
    SELECT_TELLER_CARD_INFO_BY_USER_UUID_QUERY,
    PATCH_TELLER_CARD_QUERY,
)
from common.utils.query_executor import QueryExecutor


class TellerCard(Model):
    teller_card_id = fields.BigIntField(pk=True)
    activate_badge_code = fields.CharField(max_length=255, null=True)
    activate_color_code = fields.CharField(max_length=255, null=True)

    class Meta:
        table = "teller_card"

    @classmethod
    async def get_teller_card_info_by_user_id(cls, user_id: str) -> dict | None:
        query = SELECT_TELLER_CARD_INFO_BY_USER_UUID_QUERY
        value = user_id
        return await QueryExecutor.execute_query(
            query, values=value, fetch_type="single"
        )

    @classmethod
    async def patch_teller_card_info_by_user_id(
        cls, user_id: str, badge_code: str, color_code: str
    ) -> None:
        query = PATCH_TELLER_CARD_QUERY
        values = (badge_code, color_code, user_id)
        await QueryExecutor.execute_query(query, values=values, fetch_type="single")
