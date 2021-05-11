from datetime import datetime
from fastapi import HTTPException
from app.easy_auction.auction.auction import Auction
from app.models.auction import AuctionState


class EnglishAuction(Auction):

    INC_AMT = 1.25

    def _bid_cap_reached(self, auction, bid):
        return auction.bid_cap and bid.amount >= auction.bid_cap

    def _bid(self, auction, new_bid):
        auction_session = auction.auction_session
        auction_session.bids.append(new_bid)
        auction_session.current_highest_bid = new_bid
        auction_session.last_bid_at = datetime.now()
        auction_session.bid_line = new_bid.amount + EnglishAuction.INC_AMT

        if self._bid_cap_reached(auction, new_bid):
            """
            bid_cap has reached
            """
            self.end(id)

        self.db.add(auction_session)
        self.db.commit()
        return new_bid

    def bid(self, amount, user_id):
        auction = self.db_obj
        auction_session = auction.auction_session

        if not auction_session:
            raise HTTPException(
                status_code=400,
                detail=" auction not started yet"
            )

        if auction_session.state == AuctionState.ONGOING:
            if amount > auction_session.bid_line:
                new_bid = self.create_bid(amount, user_id)
                return self._bid(auction, new_bid)
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f" bid amount must be greater than {auction_session.bid_line}"
                )
        else:
            raise HTTPException(
                status_code=400,
                detail=f" auction already {auction_session.state}"
            )
