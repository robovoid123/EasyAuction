from datetime import datetime
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session, session


from app.models.auction import AuctionState, Bid, AuctionSession, Auction as AuctionModel
from app.easy_auction.auction import Auction

from app.utils.schedule import sched
from app.crud.auction.auction import crud_auction
from app.crud.auction.auction_session import crud_auctionsession
from app.crud.product.product import crud_product
from app.crud.auction.bid import crud_bid

from app.schemas.auction import AuctionSessionCreate, AuctionSessionUpdate, AuctionUpdate, BidCreate


class EnglishAuction(Auction):

    INC_AMT = 1.25

    def _start(self, db: Session, id: int) -> AuctionSession:
        db_obj = crud_auction.get(db, id)
        sched.add_job(
            Auction.end_auction,
            'date',
            run_date=db_obj.ending_date,
            args=[id]
        )
        crud_product.reserve(db, id=db_obj.product_id, quantity=1)
        sess_obj = AuctionSessionCreate(
            state=AuctionState.ONGOING,
            bid_line=db_obj.starting_bid_amount,
            bid_cap=db_obj.bid_cap,
            reserve=db_obj.reserve,
            auction_id=db_obj.id
        )
        session_db = crud_auctionsession.create(db, obj_in=sess_obj)
        auc_obj = AuctionUpdate(starting_date=datetime.now())
        crud_auction.update(db, db_obj=db_obj, obj_in=auc_obj)
        return session_db

    def _reserve_met(self, session: AuctionSession) -> bool:
        bid: Bid = session.winning_bid
        if session.reserve and bid.amount < session.reserve:
            return False
        return True

    def _end_with_winner(self, db: Session, db_obj: AuctionModel, bid: Bid):
        auc_obj = AuctionUpdate(
            winner_id=bid.bidder_id,
            final_cost=db_obj.session.bid_line,
            is_ended=True,
        )
        crud_auction.update_with_date(
            db, db_obj=db_obj, obj_in=auc_obj, ending_date=datetime.now())
        crud_auctionsession.update_state(
            db, db_obj=db_obj.session, state=AuctionState.ENDED)

    def _end_without_winner(self, db: Session, db_obj: AuctionModel) -> None:
        auc_obj = AuctionUpdate(is_ended=True, ending_date=datetime.now())
        db.refresh(db_obj)
        crud_auction.update(db, db_obj=db_obj, obj_in=auc_obj)
        sess_obj = AuctionSessionUpdate(state=AuctionState.ENDED)
        session = db_obj.session
        db.refresh(session)
        crud_auctionsession.update(db, db_obj=session, obj_in=sess_obj)
        crud_product.free(db, db_obj.product_id, 1)

    def _end(self, db: Session, id: int) -> None:
        db_obj = crud_auction.get(db, id)
        session: AuctionSession = db_obj.session

        if session.winning_bid:
            winning_bid: Bid = session.winning_bid
            if self._reserve_met(session):
                self._end_with_winner(db, db_obj, winning_bid)
            else:
                self._end_without_winner(db, db_obj)
        else:
            self._end_without_winner(db, db_obj)

    def _bid(self, db: Session, id: int, amount: float, bidder_id: int) -> Bid:
        db_obj = crud_auction.get(db, id)
        session: AuctionSession = db_obj.session

        if amount > session.bid_line:
            new_bid_line = amount + EnglishAuction.INC_AMT
            if session.bid_cap and new_bid_line >= session.bid_cap:
                new_bid_line = session.bid_cap

            bid_obj = BidCreate(amount=amount, bidder_id=bidder_id)
            new_bid = crud_bid.create(db, obj_in=bid_obj)

            crud_auctionsession.add_bid(db, db_obj=session, bid=new_bid)
            crud_auctionsession.update(
                db, db_obj=session, obj_in=AuctionSessionUpdate(bid_line=new_bid_line))

            if session.bid_cap and new_bid.amount >= session.bid_cap:
                self.end(db, id=db_obj.id)

            return new_bid
        else:
            abl = session.bid_line
            raise HTTPException(status_code=400,
                                detail=f"bid amount must be greater than {abl}")
