from typing import Optional
from pydantic import BaseModel

from app.modules.auction.models import AuctionState


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
