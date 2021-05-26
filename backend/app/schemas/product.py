from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel
from app.models.product import Conditions


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

    class Config:
        orm_mode = True


class Product(ProductInDB):
    inventory: Optional[InventoryInDB]
    categories: Optional[List[CategoryInDB]]


class ProductUpdateRequest(BaseModel):
    name: Optional[str]
    description: Optional[str]
    condition: Optional[Conditions]
    quantity: Optional[int]
    categories: Optional[List[str]]


class ProductCreateRequest(ProductUpdateRequest):
    name: str


class ProductResponse(ProductBase):
    id: Optional[int]
    quantity: Optional[int]
    categories: Optional[List[str]]


class ProductMultiResponse(ProductInDB):
    pass
