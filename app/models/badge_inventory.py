from __future__ import annotations

from tortoise import Model, fields


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
    async def get_by_badge_code(cls, badge_code: str) -> BadgeInventory:
        return await cls.get(badge_code=badge_code)
