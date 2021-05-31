from typing import Optional, List

from pydantic import BaseModel
from .category import CategoryInDB
from app.modules.utils.schemas import ImageInDB


class ProductBase(BaseModel):
    name: Optional[str]
    description: Optional[str]


class ProductCreate(ProductBase):
    name: str


class ProductUpdate(ProductBase):
    pass


class ProductInDB(ProductBase):
    id: Optional[int]
    owner_id: Optional[int]
    categories: Optional[List[CategoryInDB]]
    images: Optional[List[ImageInDB]]

    class Config:
        orm_mode = True
