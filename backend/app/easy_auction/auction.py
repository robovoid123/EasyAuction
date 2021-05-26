from datetime import datetime

from fastapi.exceptions import HTTPException

from sqlalchemy.orm import Session
from app.schedule import sched

from app.models.auction import AuctionSession, AuctionState, Bid, Auction as AuctionModel
from app.db.session import SessionLocal
from app.schemas.auction import AuctionCreate, AuctionSessionUpdate, AuctionUpdate, BidCreate
from app.crud.auction.auction import crud_auction
from app.crud.auction.auction_session import crud_auctionsession
from app.crud.product.product import crud_product


class Auction:

    AUCTION_NOT_STARTED = HTTPException(
        status_code=400,
        detail="auction has not yet started"
    )

    ENDED_STATES = [AuctionState.ENDED, AuctionState.CANCLED]

    @classmethod
    def start_auction(cls, id: int):
        try:
            db = SessionLocal()
            auction = Auction()
            auction.start(db, id)
        finally:
            db.close()

    @classmethod
    def end_auction(cls, id: int):
        try:
            db = SessionLocal()
            auction = Auction()
            auction.end(db, id)
        finally:
            db.close()

    # TODO: if creation of auction starts to get different use this
    def create(self, db: Session, obj_in: AuctionCreate, owner_id: int, ending_date: datetime) -> AuctionModel:
        return crud_auction.create_with_owner(db, obj_in=obj_in, owner_id=owner_id, ending_date=ending_date)

    def update(self, db: Session, db_obj: AuctionModel, obj_in: AuctionUpdate) -> AuctionModel:
        return crud_auction.update(db, db_obj=db_obj, obj_in=obj_in)

    def get(self, db: Session, id: int) -> AuctionModel:
        return crud_auction.get(db, id)

    def _start(self, db: Session, id: int) -> AuctionSession:
        raise NotImplemented

    def start(self, db: Session, id: int, starting_date=None) -> AuctionSession:
        db_obj = crud_auction.get(db, id)

        if not db_obj.session:
            if starting_date:
                sched.add_job(
                    Auction.start_auction,
                    'date',
                    run_date=starting_date,
                    args=[id]
                )
            else:
                return self._start(db, id)
        else:
            raise HTTPException(status_code=400,
                                detail=f"auction already {db_obj.session.state}")

    def end(self, db: Session, id: int):
        db_obj = crud_auction.get(db, id)
        session: AuctionSession = db_obj.session
        if not db_obj.session:
            raise Auction.AUCTION_NOT_STARTED
        if session.state == AuctionState.ONGOING:
            self._end(db, id=id)
        elif session.state in Auction.ENDED_STATES:
            raise HTTPException(status_code=400,
                                detail=f"auction already ended {db_obj.session.state}")

    def _end(self, db: Session, id: int) -> None:
        raise NotImplemented

    def cancel(self, db: Session, id: int) -> AuctionSession:
        db_obj = crud_auction.get(db, id)
        session: AuctionSession = db_obj.session
        if not session:
            raise Auction.AUCTION_NOT_STARTED
        auc_obj = AuctionUpdate(is_ended=True)
        db.refresh(db_obj)
        crud_auction.update_with_date(
            db, db_obj=db_obj, obj_in=auc_obj, ending_date=datetime.now())
        sess_obj = AuctionSessionUpdate(state=AuctionState.CANCLED)
        db.refresh(session)
        crud_auctionsession.update(db, db_obj=session, obj_in=sess_obj)
        crud_product.free(db, id=db_obj.product_id, quantity=1)
        return session

    def bid(self, db: Session, id: int, amount: float, bidder_id: int) -> Bid:
        db_obj = crud_auction.get(db, id)
        session: AuctionSession = db_obj.session
        if not session:
            raise Auction.AUCTION_NOT_STARTED

        if session.state == AuctionState.ONGOING:
            return self._bid(db, id, amount=amount, bidder_id=bidder_id)
        elif session.state in Auction.ENDED_STATES:
            raise HTTPException(status_code=400,
                                detail=f"auction already {db_obj.session.state}")

    def _bid(self, db: Session, id: int, amount: float, bidder_id: int) -> Bid:
        raise NotImplemented

    def buy_it_now(self, db: Session, id: int, user_id: int) -> AuctionSession:
        db_obj = crud_auction.get(db, id)
        if not db_obj.bid_cap:
            raise HTTPException(status_code=400,
                                detail="auction does not have this feature")
        self.bid(db, id, amount=db_obj.bid_cap, bidder_id=user_id)
        return db_obj.session
