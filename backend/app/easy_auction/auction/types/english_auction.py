from datetime import datetime
from fastapi import HTTPException
from app.easy_auction.auction.auction import Auction
from app.models.auction import AuctionState


class EnglishAuction(Auction):

    INC_AMT = 1.25

    def _bid_cap_reached(self):
        return self.db_obj.bid_cap and \
            self.auction_session.current_highest_bid.amount >= self.db_obj.bid_cap

    def _bid(self, new_bid):
        self.append_bid(new_bid)

        self.update_session({
            'current_highest_bid_id': new_bid.id,
            'last_bid_at': datetime.now(),
            'bid_line': new_bid.amount + EnglishAuction.INC_AMT
        })

        if self._bid_cap_reached():
            """
            bid_cap has reached
            """
            self.end()

        return new_bid

    def bid(self, amount, user_id):
        if not self.auction_session:
            raise HTTPException(
                status_code=400,
                detail="auction not started yet"
            )

        if self.auction_session.state == AuctionState.ONGOING:
            if amount > self.auction_session.bid_line:
                new_bid = self.create_bid(amount, user_id)
                return self._bid(new_bid)
            else:
                abl = self.auction_session.bid_line
                raise HTTPException(
                    status_code=400,
                    detail=f"bid amount must be greater than {abl}"
                )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"auction already {self.auction_session.state}"
            )
