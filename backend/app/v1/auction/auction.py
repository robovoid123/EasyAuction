from datetime import datetime
from app.schedule import sched
from app.models.auction import AuctionState
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.db.session import SessionLocal
from app.easy_auction.base import Base
from app.crud.auction.auction import crud_auction
from app.easy_auction.auction.auction_session import AuctionSession
from app.easy_auction.product.product import Product

AUCTION_NOT_STARTED = HTTPException(
    status_code=400,
    detail="auction has not yet started"
)


class Auction(Base):
    def __init__(self, db: Session):
        super().__init__(crud_auction, db)
        self.auctionsession = AuctionSession(db)
        self.product = Product(db)

    def create_with_owner(self, obj_in, owner_id):
        return self.crud.create_with_owner(obj_in, owner_id)

    def _start(self, db_obj):
        sched.add_job(
            end_auction,
            'date',
            run_date=db_obj.ending_date,
            args=[id]
        )

        self.product.reserve(db_obj.product_id, 1)
        self.auctionsession.create({
            'state': AuctionState.ONGOING,
            'bid_line': db_obj.starting_bid_amount,
            'auction_id': db_obj.id
        })
        db_obj = self.get(db_obj.id)
        return self.update(db_obj, {'starting_date': datetime.now()})

    def start(self, id, starting_date=None):
        db_obj = self.get(id)
        if not db_obj.auction_session:
            if starting_date:
                sched.add_job(
                    start_auction,
                    'date',
                    run_date=starting_date,
                    args=[id]
                )
            else:
                return self._start(id)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"auction already {db_obj.auction_session.state}"
            )

    def _reserve_met(self, db_obj):
        bid = db_obj.auction_session.current_highest_bid
        if db_obj.reserve and bid.amount < db_obj.reserve:
            return False
        return True

    def _end_with_winner(self, db_obj):
        bid = db_obj.auction_session.current_highest_bid
        self.update(db_obj, {
            'winner_id': bid.bidder_id,
            'final_cost': db_obj.auction_session.bid_line,
            'is_ended': True
        })
        self.auctionsession.update(db_obj.auction_session, {
            'state': AuctionState.ENDED
        })
        return db_obj

    def _end_without_winner(self, db_obj):
        self.update(db_obj, {'is_ended': True})
        self.auctionsession.update(db_obj.auction_session, {
            'state': AuctionState.ENDED
        })
        self.product.free(db_obj.product_id, 1)
        return db_obj

    def end(self, id):
        db_obj = self.get(id)
        if not db_obj.auction_session:
            raise AUCTION_NOT_STARTED
        if db_obj.auction_session.state == AuctionState.ONGOING:
            if db_obj.auction_session.current_highest_bid:
                if self._reserve_met(db_obj):
                    return self._end_with_winner(db_obj)
                else:
                    return self._end_without_winner(db_obj)
            else:
                return self._end_without_winner(db_obj)
        elif db_obj.auction_session.state in [AuctionState.ENDED, AuctionState.CANCLED]:
            raise HTTPException(
                status_code=400,
                detail=f"auction already ended {db_obj.auction_session.state}"
            )

    def cancel(self, id):
        db_obj = self.get(id)
        if not db_obj.auction_session:
            raise AUCTION_NOT_STARTED

        self.update(db_obj, {'is_ended': True})
        self.auctionsession.update(db_obj.auction_session,
                                   {'state': AuctionState.CANCLED})
        self.product.free(db_obj.product_id, 1)
        return db_obj

    def bid(self, id, amount, bidder_id):
        db_obj = self.get(id)
        if not db_obj.auction_session:
            raise AUCTION_NOT_STARTED
        new_bid = self.auctionsession.bid(db_obj.auction_session, amount, bidder_id)

        if db_obj.bid_cap and db_obj.auction_session.bid_line >= db_obj.bid_cap:
            self.end(id)
        return new_bid

    def buy_it_now(self, id, user_id):
        db_obj = self.get(id)
        return self.bid(id, db_obj.bid_cap, user_id)


def start_auction(id):
    try:
        db = SessionLocal()
        auction = Auction(db)
        auction.start(id)
    finally:
        db.close()


def end_auction(id):
    try:
        db = SessionLocal()
        auction = Auction(db)
        auction.end(id)
    finally:
        db.close()
