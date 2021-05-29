from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class InventoryBase(BaseModel):
    quantity: Optional[int]


class InventoryCreate(InventoryBase):
    quantity: int


class InventoryUpdate(InventoryBase):
    pass


class InventoryInDB(InventoryBase):
    id: Optional[int]
    restocked_at: Optional[datetime]

    class Config:
        orm_mode = True


class Inventory(InventoryInDB):
    updated_at: Optional[datetime]
