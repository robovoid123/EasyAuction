from app.models.auction import AuctionType, AuctionState
from app.schemas.product import ProductBase
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AuctionBase(BaseModel):
    product_id: Optional[int]
    starting_bid_amount: Optional[float]
    bid_cap: Optional[float]
    reserve: Optional[float]
    ending_date: Optional[datetime]
    type: Optional[AuctionType]


class AuctionCreate(AuctionBase):
    product_id: int
    starting_bid_amount: float
    # TODO: ending_date should be > datetime.now()
    ending_date: datetime
    type: AuctionType


class AuctionUpdate(AuctionBase):
    starting_date: Optional[datetime]


class AuctionInDB(AuctionBase):
    id: Optional[int]
    owner_id: Optional[int]
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


class AuctionSessionUpdate(AuctionSessionBase):
    pass


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


class AuctionResponse(BaseModel):
    id: Optional[int]
    product: Optional[ProductBase]
    starting_bid_amount: Optional[float]
    bid_cap: Optional[float]
    reserve: Optional[float]
    ending_date: Optional[datetime]
    type: Optional[AuctionType]
    state: Optional[AuctionState]
    bid_line: Optional[float]
