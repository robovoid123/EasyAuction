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
