from typing import Optional, List

from pydantic import BaseModel
from .category import CategoryInDB
from .inventory import InventoryInDB

from app.modules.product.models import Conditions


class ProductBase(BaseModel):
    name: Optional[str]
    description: Optional[str]
    condition: Optional[Conditions]


class ProductCreate(ProductBase):
    name: str


class ProductUpdate(ProductBase):
    pass


class ProductInDB(ProductBase):
    id: Optional[int]
    owner_id: Optional[int]

    class Config:
        orm_mode = True


class Product(ProductInDB):
    pass


class ProductUpdateRequest(BaseModel):
    name: Optional[str]
    description: Optional[str]
    condition: Optional[Conditions]
    quantity: Optional[int]
    categories: Optional[List[int]]


class ProductCreateRequest(ProductUpdateRequest):
    name: str


class ProductResponse(ProductInDB):
    inventory: Optional[InventoryInDB]
    categories: Optional[List[CategoryInDB]]


class ProductMultiResponse(ProductInDB):
    pass
