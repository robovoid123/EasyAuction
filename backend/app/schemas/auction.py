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
    auction_id: Optional[int]

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
    product_id: Optional[int]

    class Config:
        orm_mode = True


class Auction(AuctionInDB):
    auction_session: Optional[AuctionSessionInDB]
    final_cost: Optional[float]
    winner_id: Optional[int]


class AuctionResponse(AuctionBase):
    id: Optional[int]
    owner_id: Optional[int]
    product_id: Optional[int]
    ending_date: Optional[datetime]
    starting_date: Optional[datetime]
    is_ended: Optional[bool]
    final_cost: Optional[float]
    winner_id: Optional[int]

    bid_line: Optional[float]
    state: Optional[AuctionState]
    last_bid_at: Optional[datetime]


class AuctionCreateRequest(AuctionCreate):
    ending_date: datetime
