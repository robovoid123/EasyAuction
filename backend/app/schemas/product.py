from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel
from app.models.product import Conditions, Service


class ProductBase(BaseModel):
    name: Optional[str]
    description: Optional[str]
    condition: Optional[Conditions]
    owner_id: Optional[int]


class ProductCreate(ProductBase):
    name: str
    owner_id: int


class ProductUpdate(ProductBase):
    pass


class ProductInDB(ProductBase):
    id: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class InventoryBase(BaseModel):
    quantity: Optional[int]


class InventoryCreate(InventoryBase):
    quantity: int


class InventoryUpdate(InventoryBase):
    restocked_at: Optional[datetime]


class InventoryInDB(InventoryBase):
    id: Optional[int]
    restocked_at: Optional[datetime]

    class Config:
        orm_mode = True


class InventoryReserveBase(BaseModel):
    quantity: Optional[int]
    reserve_in: Optional[Service]


class InventoryReserveCreate(InventoryReserveBase):
    quantity: int
    reserve_in: Service


class InventoryReserveUpdate(InventoryReserveBase):
    pass


class CategoryBase(BaseModel):
    name: Optional[str]


class CategoryCreate(CategoryBase):
    name: str


class CategoryUpdate(CategoryBase):
    pass


class CategoryInDB(CategoryBase):
    id: Optional[int]

    class Config:
        orm_mode = True


class ProductRequest(BaseModel):
    name: str
    description: Optional[str] = None
    condition: Optional[Conditions] = None
    quantity: Optional[int] = None
    categories: Optional[List[str]] = None


class ProductResponse(ProductInDB):
    categories: Optional[List[CategoryInDB]]
    inventory: Optional[InventoryInDB]
