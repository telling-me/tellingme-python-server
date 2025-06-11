from tortoise import fields
from tortoise.models import Model

from app.common.utils.query_executor import QueryExecutor
from app.dtos.teller_card.teller_card_data import TellerCardData
from app.queries.teller_card_query import (
    PATCH_TELLER_CARD_QUERY,
    SELECT_TELLER_CARD_INFO_BY_USER_UUID_QUERY,
)


class TellerCard(Model):
    teller_card_id = fields.BigIntField(primary_key=True)
    activate_badge_code = fields.CharField(max_length=255, null=True)
    activate_color_code = fields.CharField(max_length=255, null=True)

    class Meta:
        table = "teller_card"

    @classmethod
    async def get_teller_card_info_by_user_id(cls, user_id: str) -> TellerCardData:
        query = SELECT_TELLER_CARD_INFO_BY_USER_UUID_QUERY
        value = user_id
        result = await QueryExecutor.execute_query(query, values=value, fetch_type="single")
        return TellerCardData(**result)

    @classmethod
    async def patch_teller_card_info_by_user_id(
        cls, user_id: str, badge_code: str | None = None, color_code: str | None = None
    ) -> None:
        query = PATCH_TELLER_CARD_QUERY
        values = (badge_code, color_code, user_id)
        await QueryExecutor.execute_query(query, values=values, fetch_type="single")
