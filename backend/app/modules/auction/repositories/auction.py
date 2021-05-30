from app.modules.auction.models.auction_state import AuctionState
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.modules.auction.schemas import AuctionCreate, AuctionUpdate
from app.modules.auction.models import Auction
from app.repository.repository_base import BaseRepository


class AuctionRepository(BaseRepository[Auction, AuctionCreate, AuctionUpdate]):
    def create_with_owner(self, db: Session, obj_in: AuctionCreate, owner_id: int, ending_date: datetime) -> Auction:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id,
                            ending_date=ending_date)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_with_date(self, db: Session, db_obj: Auction,
                         obj_in: AuctionUpdate, ending_date: datetime) -> Auction:
        return self.update(db, db_obj=db_obj, obj_in={
            **obj_in.dict(exclude_unset=True), 'ending_date': ending_date})

    def change_state(self, db: Session, db_obj: Auction, state: AuctionState):
        db_obj.state = state
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)


auction_repo = AuctionRepository(Auction)
