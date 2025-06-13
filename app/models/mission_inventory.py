from tortoise import Model, fields
from tortoise.transactions import in_transaction


class MissionInventory(Model):
    mission_inventory_id = fields.BigIntField(primary_key=True)
    condition_type = fields.CharField(max_length=255)
    mission_code = fields.CharField(max_length=255)
    mission_description = fields.CharField(max_length=255)
    mission_name = fields.CharField(max_length=255)
    reward_code = fields.CharField(max_length=255)
    target_count = fields.IntField()

    class Meta:
        table = "mission_inventory"

    @classmethod
    async def create_bulk(cls) -> None:
        data = [
            (1, "하", "MS_LV_UP", "XP를 누적하여 다음 레벨에 도달했어요!", "레벨 업 달성", "RW_LV_000", 1),
            (2, "하", "MS_BADGE_POST_FIRST", "첫 글을 첫 글을 작성했어요!", "첫 글 작성", "RW_FIRST_POST", 1),
            (3, "하", "MS_BADGE_POST_280_CHAR", "280자 이상 글을 1회 작성했어요!", "긴 글 작성", "RW_LONG_POST", 1),
            (
                4,
                "하",
                "MS_BADGE_POST_CONSECUTIVE_7",
                "연속으로 7일 작성했어요!",
                "연속 7일 글 작성",
                "RW_CONSECUTIVE_7",
                1,
            ),
            (
                5,
                "하",
                "MS_BADGE_POST_EARLY_3",
                "새벽 시간에 글 3회 작성했어요!",
                "이른 아침 작가",
                "RW_EARLY_MORNING",
                3,
            ),
            (
                6,
                "하",
                "MS_DAILY_LIKE_3_PER_DAY",
                "하루에 다른 글 3개에 좋아요를 누르세요",
                "하루 좋아요 3개",
                "RW_LIKE_3_DAY",
                1,
            ),
            (7, "중", "MS_BADGE_CHEESE_TOTAL_50", "치즈 50개를 모았어요!", "치즈 수집가", "RW_CHEESE_50", 1),
            (8, "하", "MS_BADGE_REGISTRATION", "회원가입 보상이에요!", "환영 뱃지", "RW_REGISTRATION", 1),
            (9, "하", "MS_BADGE_CHRISTMAS", "2024 크리스마스 한정판 배지예요!", "크리스마스 뱃지", "RW_CHRISTMAS", 1),
            (10, "하", "MS_SINGLE_POST_2_5", "2~5회의 기록을 작성했어요!", "2~5 글 작성", "RW_POST_2_5", 1),
            (11, "하", "MS_DAILY_POST_GENERAL", "기록을 작성했어요!", "일반 작성 보상", "RW_POST_GENERAL", 1),
        ]

        async with in_transaction():
            await cls.bulk_create(
                [
                    cls(
                        mission_inventory_id=mid,
                        condition_type=ctype,
                        mission_code=mcode,
                        mission_description=desc,
                        mission_name=name,
                        reward_code=rcode,
                        target_count=target,
                    )
                    for mid, ctype, mcode, desc, name, rcode, target in data
                ]
            )
