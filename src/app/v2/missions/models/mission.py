from tortoise import fields
from tortoise.models import Model

from app.v2.missions.querys.mission_query import SELECT_USER_MISSIONS_QUERY, UPDATE_USER_MISSION_PROGRESS_QUERY
from common.utils.query_executor import QueryExecutor


class UserMission(Model):
    user_mission_id = fields.BigIntField(pk=True)
    is_completed = fields.BooleanField(default=False)
    mission_code = fields.CharField(max_length=255)
    progress_count = fields.IntField(default=0)
    user = fields.ForeignKeyField("models.User", related_name="missions")

    @classmethod
    async def get_user_missions_by_condition_type(cls, user_id: str) -> dict:
        query = SELECT_USER_MISSIONS_QUERY
        values = (user_id,)
        return await QueryExecutor.execute_query(query, values=values, fetch_type="multiple")

    @classmethod
    async def update_user_mission_progress(
        cls,
        user_id: str,
        mission_code: str,
        new_progress_count: int,
        is_completed: bool,
    ) -> None:
        query = UPDATE_USER_MISSION_PROGRESS_QUERY
        values = (new_progress_count, int(is_completed), user_id, mission_code)
        await QueryExecutor.execute_query(query, values=values, fetch_type="single")


class MissionInventory(Model):
    mission_inventory_id = fields.BigIntField(pk=True)
    condition_type = fields.CharField(max_length=255)
    mission_code = fields.CharField(max_length=255)
    mission_description = fields.CharField(max_length=255)
    mission_name = fields.CharField(max_length=255)
    reward_code = fields.CharField(max_length=255)
    target_count = fields.IntField()

    class Meta:
        table = "mission_inventory"
