from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.crud.base import CRUDBase
from app.schemas import auction as ap
from app.models.auction import Auction, AuctionSession, Bid


class CRUDAuction(CRUDBase[Auction, ap.AuctionCreate, ap.AuctionUpdate]):

    def create_auction_session(self, db, obj_in: ap.AuctionSessionCreate):

        obj_in_data = jsonable_encoder(obj_in)

        db_obj = AuctionSession(**obj_in_data)  # type: ignore

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def create_bid(self, db: Session, amount, bidder_id):

        db_obj = Bid(amount=amount, bidder_id=bidder_id)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj


auction = CRUDAuction(Auction)
