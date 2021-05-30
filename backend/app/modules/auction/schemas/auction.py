from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class AuctionBase(BaseModel):
    starting_amount: Optional[float]
    bid_cap: Optional[float]
    reserve: Optional[float]


class AuctionCreate(AuctionBase):
    product_id: int
    owner_id: int
    starting_amount: float


class AuctionUpdate(AuctionBase):
    pass


class AuctionInDB(AuctionBase):
    id: Optional[int]
    owner_id: Optional[int]
    product_id: Optional[int]

    class Config:
        orm_mode = True
