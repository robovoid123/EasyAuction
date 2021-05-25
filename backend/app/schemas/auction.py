from app.models.auction import AuctionType, AuctionState
from app.schemas.product import ProductInDB
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BidBase(BaseModel):
    amount: Optional[float]
    bidder_id: Optional[int]


class BidCreate(BidBase):
    amount: float
    bidder_id: int


class BidUpdate(BidBase):
    pass


class BidInDB(BidBase):
    id: Optional[int]

    class Config:
        orm_mode = True


class AuctionSessionBase(BaseModel):
    state: Optional[AuctionState]
    bid_line: Optional[float]
    bid_cap: Optional[float]
    reserve: Optional[float]


class AuctionSessionCreate(AuctionSessionBase):
    state: AuctionState
    bid_line: float
    auction_id: int
    bid_cap: float
    reserve: float


class AuctionSessionUpdate(AuctionSessionBase):
    winning_bid_id: Optional[int]


class AuctionSessionInDB(AuctionSessionBase):
    id: Optional[int]
    last_bid_at: Optional[datetime]
    winning_bid: Optional[BidInDB]

    class Config:
        orm_mode = True


class AuctionBase(BaseModel):
    starting_bid_amount: Optional[float]
    bid_cap: Optional[float]
    reserve: Optional[float]
    au_type: Optional[AuctionType]


class AuctionCreate(AuctionBase):
    product_id: int
    starting_bid_amount: float
    au_type: AuctionType


class AuctionUpdate(AuctionBase):
    is_ended: Optional[bool]
    final_cost: Optional[float]
    winner_id: Optional[int]


class AuctionInDB(AuctionBase):
    id: Optional[int]
    owner_id: Optional[int]
    starting_date: Optional[datetime]
    product: Optional[ProductInDB]
    auction_session: Optional[AuctionSessionInDB]
    final_cost: Optional[float]
    winner_id: Optional[int]

    class Config:
        orm_mode = True


class AuctionCreateRequest(AuctionCreate):
    pass
