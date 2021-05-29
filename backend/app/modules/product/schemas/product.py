from typing import Optional, List

from pydantic import BaseModel

from app.modules.product.models import Conditions

from .category import CategoryInDB
from .inventory import InventoryInDB


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


class ProductCreateRequest(ProductUpdateRequest):
    name: str
    categories: Optional[List[int]]
    quantity: Optional[int]


class ProductResponse(ProductInDB):
    inventory: Optional[InventoryInDB]
    categories: Optional[List[CategoryInDB]]


class ProductMultiResponse(ProductInDB):
    pass
