from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.modules.auction.models import AuctionType, AuctionState
from .auction_session import AuctionSessionInDB


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
