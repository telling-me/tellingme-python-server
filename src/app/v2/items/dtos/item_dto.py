# schemas.py
from typing import Optional

from pydantic import BaseModel


class ItemInventorySchema(BaseModel):
    item_category: Optional[str]
    item_code: Optional[str]


class ProductInventorySchema(BaseModel):
    price: Optional[float]
    product_category: Optional[str]
    product_code: Optional[str]
    transaction_currency: Optional[str]


class ItemInventoryProductInventorySchema(BaseModel):
    quantity: int
    item_measurement: Optional[str]
    item_inventory_id: int
    product_inventory_id: int
