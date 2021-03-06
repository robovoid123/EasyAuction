from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from app.modules.product.schemas.product import ProductInDB


class AuctionBase(BaseModel):
    starting_amount: Optional[float]
    bid_cap: Optional[float]
    reserve: Optional[float]


class AuctionCreate(AuctionBase):
    product_id: int
    starting_amount: float = Field(..., gt=0)


class AuctionUpdate(AuctionBase):
    pass


class AuctionInDB(AuctionBase):
    id: Optional[int]
    owner_id: Optional[int]
    product: Optional[ProductInDB]
    state: Optional[str]
    current_bid_amount: Optional[float]
    last_bid_at: Optional[datetime]
    final_winner_id: Optional[int]
    starting_date: Optional[datetime]
    ending_date: Optional[datetime]
    bid_count: Optional[int]

    class Config:
        orm_mode = True
