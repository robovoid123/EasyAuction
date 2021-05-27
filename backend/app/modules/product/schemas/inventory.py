from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class InventoryBase(BaseModel):
    quantity: Optional[int]


class InventoryCreate(InventoryBase):
    quantity: int


class InventoryUpdate(InventoryBase):
    restocked_at: Optional[datetime]


class InventoryInDB(InventoryBase):
    id: Optional[int]

    class Config:
        orm_mode = True


class Inventory(InventoryInDB):
    updated_at: Optional[datetime]
