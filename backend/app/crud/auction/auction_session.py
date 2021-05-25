from datetime import datetime
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.schemas import auction as ap
from app.models.auction import AuctionSession, AuctionState, Bid


class CRUDAuctionSession(CRUDBase[AuctionSession, ap.AuctionSessionCreate,
                                  ap.AuctionSessionUpdate]):
    def update_with_date(self, db: Session, *,
                         db_obj: AuctionSession, obj_in: ap.AuctionSessionUpdate, last_bid_at: datetime) -> AuctionSession:

        return self.update(db, db_obj=db_obj, obj_in={
            **obj_in.dict(exclude_unset=True), 'last_bid_at': last_bid_at})

    def add_bid(self, db: Session, *, db_obj: AuctionSession,
                bid: Bid):
        db_obj.bids.append(bid)
        db_obj.last_bid_at = datetime.now()
        db_obj.winning_bid_id = bid.id
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_state(self, db: Session, db_obj: AuctionSession, state: AuctionState):
        db_obj.state = state
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


crud_auctionsession = CRUDAuctionSession(AuctionSession)
