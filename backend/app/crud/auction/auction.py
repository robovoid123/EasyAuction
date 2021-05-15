from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.crud.base import CRUDBase
from app.schemas import auction as ap
from app.models.auction import Auction


class CRUDAuction(CRUDBase[Auction, ap.AuctionCreate, ap.AuctionUpdate]):
    def create_with_owner(self, db: Session, obj_in, owner_id):
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


crud_auction = CRUDAuction(Auction)
