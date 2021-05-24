from datetime import datetime
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.crud.base import CRUDBase
from app.schemas import auction as ap
from app.models.auction import Auction


class CRUDAuction(CRUDBase[Auction, ap.AuctionCreate, ap.AuctionUpdate]):
    def create_with_owner(self, db: Session, obj_in: ap.AuctionCreate, owner_id: int, ending_date: datetime) -> Auction:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id,
                            ending_date=ending_date)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_with_date(self, db: Session, db_obj: Auction,
                         obj_in: ap.AuctionUpdate, ending_date: datetime) -> Auction:
        return self.update(db, db_obj=db_obj, obj_in={
            **obj_in.dict(), 'ending_date': ending_date})


crud_auction = CRUDAuction(Auction)
