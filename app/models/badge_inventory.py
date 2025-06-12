from __future__ import annotations

from tortoise import Model, fields
from tortoise.transactions import in_transaction


class BadgeInventory(Model):
    badge_code = fields.CharField(max_length=255, primary_key=True)
    badge_name = fields.CharField(max_length=255, null=True)
    badge_condition = fields.CharField(max_length=255, null=True)
    badge_middle_name = fields.CharField(max_length=255, null=True)

    class Meta:
        table = "badge_inventory"

    @property
    def badge_full_name(self) -> str:
        return f"{self.badge_middle_name} {self.badge_name}"

    @classmethod
    async def create_bulk(cls) -> None:
        badges = [
            cls(
                badge_code="BG_AGAIN_001",
                badge_condition="연속으로 7일 작성했어요!",
                badge_middle_name="또 오셨네요,",
                badge_name="단골 텔러",
            ),
            cls(
                badge_code="BG_CHRISTMAS_2024",
                badge_condition="2024 크리스마스 한정판 배지예요!",
                badge_middle_name="흰 눈 사이에서,",
                badge_name="화이트 크리스마스",
            ),
            cls(
                badge_code="BG_FIRST",
                badge_condition="첫 글을 작성했어요!",
                badge_middle_name="낯선 길에 첫 발자국,",
                badge_name="탐험가 텔러",
            ),
            cls(
                badge_code="BG_MUCH_001",
                badge_condition="280자 이상 글을 1회 작성했어요!",
                badge_middle_name="내 이야길 들어봐,",
                badge_name="투머치 토커",
            ),
            cls(
                badge_code="BG_NEW",
                badge_condition="회원가입 시 기본 제공",
                badge_middle_name="아직은 낯설어요,",
                badge_name="미스터리 방문객",
            ),
            cls(
                badge_code="BG_NIGHT_001",
                badge_condition="새벽 시간에 글 3회 작성했어요!",
                badge_middle_name="다들 꿈꿀 때 글을 썼지,",
                badge_name="올빼미 텔러",
            ),
            cls(
                badge_code="BG_SAVE_001",
                badge_condition="치즈 50개를 모았어요!",
                badge_middle_name="치즈를 모아모아,",
                badge_name="나는야 저축왕",
            ),
        ]
        async with in_transaction():
            await cls.bulk_create(badges)

    @classmethod
    async def get_by_badge_code(cls, badge_code: str) -> BadgeInventory:
        return await cls.get(badge_code=badge_code)
