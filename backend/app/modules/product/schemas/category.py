from typing import Optional

from pydantic import BaseModel


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
