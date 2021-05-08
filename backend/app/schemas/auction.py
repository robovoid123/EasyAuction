from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AuctionBase(BaseModel):
    product_id: Optional[int]
    owner_id: Optional[int]
    starting_bid_amount: Optional[float]
    bid_cap: Optional[float]
    reserve: Optional[float]
    ending_date: Optional[datetime]
    type: Optional[str]


class AuctionCreate(AuctionBase):
    product_id: int
    owner_id: int
    starting_bid_amount: float
    ending_date: datetime
    type: str


class AuctionUpdate(AuctionBase):
    pass


class AuctionInDB(AuctionBase):
    id: Optional[int]
    starting_date: Optional[datetime]

    class Config:
        orm_mode = True


class AuctionSessionBase(BaseModel):
    state: Optional[str]
    bid_line: Optional[float]
    auction_id: Optional[int]


class AuctionSessionCreate(AuctionSessionBase):
    state: str
    bid_line: float
    auction_id: int


class BidBase(BaseModel):
    amount: Optional[float]
    bidder_id: Optional[int]


class BidInDB(BidBase):
    id: Optional[int]

    class Config:
        orm_mode = True
