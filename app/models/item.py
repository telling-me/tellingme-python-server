from tortoise import fields
from tortoise.fields import ForeignKeyRelation
from tortoise.models import Model
from tortoise.transactions import in_transaction


class ItemInventory(Model):
    item_id = fields.BigIntField(primary_key=True)
    item_category = fields.CharField(max_length=255, null=True)
    item_code = fields.CharField(max_length=255, null=True)

    class Meta:
        table = "item_inventory"

    @classmethod
    async def create_bulk(cls) -> None:
        items_data = [
            (1, "BADGE", "BG_AGAIN_001"),
            (2, "BADGE", "BG_CHRISTMAS_2024"),
            (3, "BADGE", "BG_FIRST"),
            (4, "BADGE", "BG_MUCH_001"),
            (5, "BADGE", "BG_NEW"),
            (6, "BADGE", "BG_NIGHT_001"),
            (7, "BADGE", "BG_SAVE_001"),
            (16, "COLOR", "CL_BLUE_001"),
            (17, "COLOR", "CL_DEFAULT"),
            (18, "COLOR", "CL_GREEN_001"),
            (19, "COLOR", "CL_NAVY_001"),
            (20, "COLOR", "CL_ORANGE_001"),
            (21, "COLOR", "CL_PINK_001"),
            (22, "COLOR", "CL_PURPLE_001"),
            (23, "COLOR", "CL_RED_001"),
            (24, "COLOR", "CL_YELLOW_001"),
            (25, "EMOTION", "EM_HAPPY"),
            (26, "EMOTION", "EM_PROUD"),
            (27, "EMOTION", "EM_OKAY"),
            (28, "EMOTION", "EM_TIRED"),
            (29, "EMOTION", "EM_SAD"),
            (30, "EMOTION", "EM_ANGRY"),
            (31, "EMOTION", "EM_EXCITED"),
            (32, "EMOTION", "EM_FUN"),
            (33, "EMOTION", "EM_RELAXED"),
            (34, "EMOTION", "EM_APATHETIC"),
            (35, "EMOTION", "EM_LONELY"),
            (36, "EMOTION", "EM_COMPLEX"),
            (37, "SUBSCRIPTION", "PLUS_MONTH_1"),
            (38, "SUBSCRIPTION", "PLUS_YEAR_1"),
            (39, "CHEESE", "CHEESE"),
            (40, "POINT", "POINT"),
        ]

        async with in_transaction():
            await cls.bulk_create(
                [cls(item_id=item_id, item_category=category, item_code=code) for item_id, category, code in items_data]
            )


class ProductInventory(Model):
    product_id = fields.BigIntField(primary_key=True)
    price = fields.FloatField(null=True)
    product_category = fields.CharField(max_length=255, null=True)
    product_code = fields.CharField(max_length=255, null=True)
    transaction_currency = fields.CharField(max_length=255, null=True)

    class Meta:
        table = "product_inventory"

    @classmethod
    async def create_bulk(cls) -> None:
        products_data = [
            (1, 20, "CONSUMABLE", "PD_CL_PURPLE_001", "CHEESE"),
            (2, 20, "CONSUMABLE", "PD_CL_NAVY_001", "CHEESE"),
            (3, 20, "CONSUMABLE", "PD_CL_PINK_001", "CHEESE"),
            (4, 20, "CONSUMABLE", "PD_CL_YELLOW_001", "CHEESE"),
            (5, 20, "CONSUMABLE", "PD_CL_GREEN_001", "CHEESE"),
            (6, 33, "CONSUMABLE", "PD_EM_EXCITED", "CHEESE"),
            (7, 33, "CONSUMABLE", "PD_EM_FUN", "CHEESE"),
            (8, 33, "CONSUMABLE", "PD_EM_RELAXED", "CHEESE"),
            (9, 33, "CONSUMABLE", "PD_EM_APATHETIC", "CHEESE"),
            (10, 33, "CONSUMABLE", "PD_EM_LONELY", "CHEESE"),
            (11, 33, "CONSUMABLE", "PD_EM_COMPLEX", "CHEESE"),
            (12, 990, "SUBSCRIPTION", "PD_PLUS_MONTH_1_KR", "KRW"),
            (13, 9900, "SUBSCRIPTION", "PD_PLUS_YEAR_1_KR", "KRW"),
            (14, 33, "CONSUMABLE", "PD_BG_CHRISTMAS_2024", "CHEESE"),
            (15, 0, "CONSUMABLE", "PD_TEST", "CHEESE"),
        ]

        async with in_transaction():
            await cls.bulk_create(
                [
                    cls(
                        product_id=pid,
                        price=price,
                        product_category=category,
                        product_code=code,
                        transaction_currency=currency,
                    )
                    for pid, price, category, code, currency in products_data
                ]
            )


class ItemInventoryProductInventory(Model):
    item_inventory_product_inventory_id = fields.BigIntField(primary_key=True)
    quantity = fields.IntField()
    item_inventory: ForeignKeyRelation[ItemInventory] = fields.ForeignKeyField(
        "models.ItemInventory", related_name="product_inventories"
    )
    product_inventory: ForeignKeyRelation[ProductInventory] = fields.ForeignKeyField(
        "models.ProductInventory", related_name="item_inventories"
    )
    item_measurement = fields.CharField(max_length=255, null=True)

    class Meta:
        table = "item_inventory_product_inventory"

    @classmethod
    async def create_bulk(cls) -> None:
        mapping_data = [
            (1, 1, 22, 1, "UNIT"),
            (2, 1, 19, 2, "UNIT"),
            (3, 1, 21, 3, "UNIT"),
            (4, 1, 24, 4, "UNIT"),
            (5, 1, 18, 5, "UNIT"),
            (6, 1, 31, 6, "UNIT"),
            (7, 1, 32, 7, "UNIT"),
            (8, 1, 33, 8, "UNIT"),
            (9, 1, 34, 9, "UNIT"),
            (10, 1, 35, 10, "UNIT"),
            (11, 1, 36, 11, "UNIT"),
            (12, 1, 37, 12, "MONTH"),
            (13, 1, 38, 13, "YEAR"),
            (14, 1, 2, 14, "UNIT"),
        ]

        async with in_transaction():
            await cls.bulk_create(
                [
                    cls(
                        item_inventory_product_inventory_id=id_,
                        quantity=quantity,
                        item_inventory_id=item_id,
                        product_inventory_id=product_id,
                        item_measurement=measurement,
                    )
                    for id_, quantity, item_id, product_id, measurement in mapping_data
                ]
            )


class RewardInventory(Model):
    reward_inventory_id = fields.BigIntField(primary_key=True)
    item_code = fields.CharField(max_length=255, null=True)
    reward_code = fields.CharField(max_length=255, null=True)
    reward_description = fields.CharField(max_length=255, null=True)
    reward_name = fields.CharField(max_length=255, null=True)

    item_inventories = fields.ReverseRelation["ItemInventoryRewardInventory"]

    class Meta:
        table = "reward_inventory"

    @classmethod
    async def create_bulk(cls) -> None:
        rewards_data = [
            (1, "RW_LV_000", "레벨업 보상"),
            (2, "RW_FIRST_POST", "첫 글 작성 보상"),
            (3, "RW_LONG_POST", "280자 이상의 글을 작성 보상"),
            (4, "RW_CONSECUTIVE_7", "연속 7일 글 작성 보상"),
            (5, "RW_EARLY_MORNING", "오전 12시~6시에 3개의 글 작성 보상"),
            (6, "RW_LIKE_3_DAY", "하루 좋아요 3개"),
            (7, "RW_CHEESE_50", "누적 치즈 50개를 획득하세요"),
            (8, "RW_REGISTRATION", "회원가입 보상"),
            (9, "RW_CHRISTMAS", "크리스마스 시즌에 접속하여 뱃지를 받으세요"),
            (10, "RW_POST_2_5", "글 작성 보상 2~5개"),
            (11, "RW_POST_GENERAL", "글 작성 보상"),
        ]

        async with in_transaction():
            await cls.bulk_create(
                [
                    cls(
                        reward_inventory_id=reward_id,
                        reward_code=code,
                        reward_description=desc,
                        reward_name=None,
                        item_code=None,
                    )
                    for reward_id, code, desc in rewards_data
                ]
            )


class ItemInventoryRewardInventory(Model):
    item_inventory_reward_invnetory_id = fields.BigIntField(primary_key=True)
    quantity = fields.IntField()
    item_inventory: ForeignKeyRelation[ItemInventory] = fields.ForeignKeyField(
        "models.ItemInventory",
        related_name="reward_inventories",
        on_delete=fields.CASCADE,
        db_column="item_inventory_id",
    )
    reward_inventory: ForeignKeyRelation[RewardInventory] = fields.ForeignKeyField(
        "models.RewardInventory",
        related_name="item_inventories",
        on_delete=fields.CASCADE,
        db_column="reward_inventory_id",
    )
    item_measurement = fields.CharField(max_length=255, null=True)

    class Meta:
        table = "item_inventory_reward_inventory"

    @classmethod
    async def create_bulk(cls) -> None:
        data = [
            (1, 1, 39, 1, "UNIT"),
            (2, 1, 39, 2, "UNIT"),
            (3, 1, 3, 2, "UNIT"),
            (4, 1, 4, 3, "UNIT"),
            (5, 1, 1, 4, "UNIT"),
            (6, 1, 6, 5, "UNIT"),
            (7, 1, 40, 6, "UNIT"),
            (8, 1, 7, 7, "UNIT"),
            (9, 1, 5, 8, "UNIT"),
            (10, 1, 2, 9, "UNIT"),
            (11, 1, 23, 9, "UNIT"),
            (12, 5, 40, 10, "UNIT"),
            (13, 5, 39, 3, "UNIT"),
            (14, 5, 39, 4, "UNIT"),
            (15, 5, 39, 5, "UNIT"),
            (16, 10, 39, 7, "UNIT"),
        ]

        async with in_transaction():
            await cls.bulk_create(
                [
                    cls(
                        item_inventory_reward_invnetory_id=pk,
                        quantity=qty,
                        item_inventory_id=item_id,
                        reward_inventory_id=reward_id,
                        item_measurement=measure,
                    )
                    for pk, qty, item_id, reward_id, measure in data
                ]
            )
