from app.repository.repository_base import BaseRepository
from datetime import datetime
from sqlalchemy.orm import Session
from app.modules.auction.schemas import AuctionSessionCreate, AuctionSessionUpdate
from app.modules.auction.models import AuctionSession, AuctionState, Bid


class AuctionSessionRepository(BaseRepository[AuctionSession, AuctionSessionCreate,
                                              AuctionSessionUpdate]):
    def update_with_date(self, db: Session, *,
                         db_obj: AuctionSession, obj_in: AuctionSessionUpdate, last_bid_at: datetime) -> AuctionSession:

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


auction_session_repo = AuctionSessionRepository(AuctionSession)
