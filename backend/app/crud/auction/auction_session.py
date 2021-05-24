from datetime import datetime
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.schemas import auction as ap
from app.models.auction import AuctionSession


class CRUDAuctionSession(CRUDBase[AuctionSession, ap.AuctionSessionCreate,
                                  ap.AuctionSessionUpdate]):
    def update_with_date(self, db: Session, *,
                         db_obj: AuctionSession, obj_in: ap.AuctionSessionUpdate, last_bid_at: datetime) -> AuctionSession:

        return self.update(db, db_obj=db_obj, obj_in={
            **obj_in.dict(), 'last_bid_at': last_bid_at})


crud_auctionsession = CRUDAuctionSession(AuctionSession)
