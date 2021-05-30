from typing import Optional

from pydantic import BaseModel


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

    class Config:
        orm_mode = True
