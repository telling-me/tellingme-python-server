from tortoise import fields
from tortoise.fields import ForeignKeyRelation
from tortoise.models import Model

from app.common.utils.query_executor import QueryExecutor
from app.dtos.mission.mission_data import MissionData
from app.models.user import User
from app.queries.mission_query import SELECT_USER_MISSIONS_QUERY, UPDATE_USER_MISSION_PROGRESS_QUERY


class UserMission(Model):
    user_mission_id = fields.BigIntField(primary_key=True)
    is_completed = fields.BooleanField(default=False)
    mission_code = fields.CharField(max_length=255)
    progress_count = fields.IntField(default=0)
    user: ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", related_name="missions")

    class Meta:
        table = "user_mission"

    @classmethod
    async def get_user_missions_by_condition_type(cls, user_id: str) -> list[MissionData]:
        query = SELECT_USER_MISSIONS_QUERY
        values = (user_id,)
        results = await QueryExecutor.execute_query(query, values=values, fetch_type="multiple")
        return [
            MissionData(
                user_mission_id=row.get("user_mission_id", 0),
                mission_code=row.get("mission_code", ""),
                progress_count=row.get("progress_count", 0),
                is_completed=MissionData.to_bool(row.get("is_completed")),
            )
            for row in results
        ]

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
