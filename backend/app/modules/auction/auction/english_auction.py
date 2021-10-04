from datetime import date, datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.modules.auction.models.auction_state import AuctionState
from app.modules.auction.models.auction import Auction
from app.modules.auction.repositories import bid_repo, auction_repo
from app.modules.auction.schemas.bid import BidCreate
from app.utils.schedule import sched
from app.db.session import SessionLocal

INC_AMT = 1.25

INVALID_BID_EXCEPTION = HTTPException(status_code=400,
                                      detail="Bid needs to be greater than Current Highest Bid")


AUCTION_NOT_STARTED_EXCEPTION = HTTPException(
    status_code=400,
    detail='Auction has not yet been started'
)


class EnglishAuction:
    @classmethod
    def start_auction(cls, id: int):
        try:
            db = SessionLocal()
            english = EnglishAuction()
            auction = auction_repo.get(db, id=id)
            english.start(db, db_obj=auction)
        finally:
            db.close()

    @classmethod
    def end_auction(cls, id: int):
        try:
            db = SessionLocal()
            english = EnglishAuction()
            auction = auction_repo.get(db, id=id)
            english.end(db, db_obj=auction)
        finally:
            db.close()

    def is_valid_bid(self, db_obj: Auction, amount):
        return amount > db_obj.current_bid_amount

    def bid(self, db: Session, db_obj: Auction, amount: float, bidder_id: int):
        if not self.is_valid_bid(db_obj=db_obj, amount=amount):
            raise INVALID_BID_EXCEPTION

        if db_obj.state != AuctionState.ONGOING:
            raise AUCTION_NOT_STARTED_EXCEPTION

        new_bid = bid_repo.create(db, obj_in=BidCreate(
            amount=amount,
            bidder_id=bidder_id
        ))
        db_obj.bids.append(new_bid)
        db_obj.last_bid_at = datetime.now()
        db_obj.winning_bid_id = new_bid.id
        db_obj.bid_count += 1

        if db_obj.bid_cap and amount >= db_obj.bid_cap:
            db_obj.current_bid_amount = db_obj.bid_cap
            db_obj.final_winner_id = bidder_id
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            self.end(db, db_obj=db_obj)
        else:
            db_obj.current_bid_amount = amount + INC_AMT
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)

    def buy_it_now(self, db: Session, db_obj: Auction, buyer_id: int):
        db_obj.current_bid_amount = db_obj.bid_cap
        db_obj.final_winner_id = buyer_id
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        self.end(db, db_obj=db_obj)

    def start(self, db: Session, db_obj: Auction, ending_date, starting_date=None) -> Auction:
        auction_id = db_obj.id
        if starting_date:
            # schedule start of auction
            sched.add_job(
                EnglishAuction.start_auction,
                'date',
                run_date=starting_date,
                args=[auction_id]
            )
            db_obj.starting_date = starting_date
        else:
            db_obj.starting_date = datetime.now()

        # schedule ending
        sched.add_job(
            EnglishAuction.end_auction,
            'date',
            run_date=ending_date,
            args=[auction_id]
        )

        db_obj.current_bid_amount = db_obj.starting_amount
        db_obj.ending_date = ending_date
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        auction_repo.change_state(db, db_obj=db_obj, state=AuctionState.ONGOING)
        return db_obj

    def end(self, db: Session, db_obj: Auction) -> Auction:
        if db_obj.reserve and db_obj.current_bid_amount < db_obj.reserve:
            auction_repo.change_state(db, db_obj=db_obj, state=AuctionState.CANCLED)
        else:
            if db_obj.winning_bid:
                db_obj.final_winner_id = db_obj.winning_bid.bidder_id
                db.add(db_obj)
                db.commit()
                db.refresh(db_obj)
            auction_repo.change_state(db, db_obj=db_obj, state=AuctionState.ENDED)
        return db_obj

    def cancel(self, db: Session, db_obj: Auction):
        return auction_repo.change_state(db, db_obj=db_obj, state=AuctionState.CANCLED)
