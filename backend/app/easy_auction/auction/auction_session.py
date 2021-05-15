from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.easy_auction.base import Base
from app.crud.auction.auction_session import crud_auctionsession
from app.easy_auction.auction.bid import Bid
from app.models.auction import AuctionState

INC_AMT = 1.25


class AuctionSession(Base):
    def __init__(self, db: Session):
        super().__init__(crud_auctionsession, db)

        self._bid = Bid(db)

    def bid(self, db_obj, amount, bidder_id):
        if db_obj.state == AuctionState.ONGOING:
            if amount > db_obj.bid_line:
                new_bid_line = amount + INC_AMT
                if new_bid_line >= db_obj.auction.bid_cap:
                    new_bid_line = db_obj.auction.bid_cap

                new_bid = self._bid.create({
                    'amount': amount,
                    'bidder_id': bidder_id,
                    'session_id': db_obj.id
                })
                db_obj = self.get(db_obj.id)
                self.update(db_obj, {
                    'current_highest_bid_id': new_bid.id,
                    'last_bid_at': datetime.now(),
                    'bid_line': new_bid_line
                })
                return new_bid
            else:
                abl = db_obj.bid_line
                raise HTTPException(
                    status_code=400,
                    detail=f"bid amount must be greater than {abl}"
                )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"auction already {db_obj.state}"
            )
