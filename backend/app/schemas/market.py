# from app.schemas.product import ProductBase
# from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ShopBase(BaseModel):
    name: Optional[str]
    description: Optional[str]
    owner_id: Optional[int]


class ShopCreate(ShopBase):
    name: str
    owner_id: int


class ShopUpdate(ShopBase):
    pass


class PublishedProductBase(BaseModel):
    price: Optional[float]
    quantity: Optional[int]
    product_id: Optional[int]


class PublishedProductCreate(PublishedProductBase):
    price: float
    quantity: int
    product_id: int


class PublishedProductUpdate(PublishedProductBase):
    pass


class PublishedProductLogBase(BaseModel):
    quantity: Optional[float]
    product_id: Optional[int]
    buyer_id: Optional[int]


class PublishedProductLogCreate(PublishedProductLogBase):
    quantity: float
    product_id: int
    buyer_id: int


class PublishedProductLogUpdate(PublishedProductLogBase):
    pass
