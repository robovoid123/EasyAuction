from typing import List
from app.modules.auction.models.auction_state import AuctionState
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException

from app.modules.auction.schemas import AuctionCreate, AuctionUpdate
from app.modules.auction.models import Auction
from app.repository.repository_base import BaseRepository
from app.modules.product.models.product import Product


INVALID_ORDER_BY_EXCEPTION = HTTPException(status_code=400,
                                           detail="can't order by the given value")


class AuctionRepository(BaseRepository[Auction, AuctionCreate, AuctionUpdate]):
    def __init__(self, model):
        super().__init__(model)

        self.order_by_columns = {
            "bid_count": model.bid_count,
            "starting_bid_amount": model.starting_amount,
            "bid_cap": model.bid_cap,
            "starting_date": model.starting_date,
            "ending_date": model.ending_date,
            "last_bid_at": model.last_bid_at,
            "reserve": model.reserve
        }

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100, like: str = None, states: List[str], order_by: str):
        order_by_column = self.order_by_columns.get(order_by)
        if not order_by_column:
            raise INVALID_ORDER_BY_EXCEPTION
        auctions = db.query(self.model).join(Product)
        if like:
            auctions = auctions.filter(Product.name.like('%' + like + '%'))
        return auctions.filter(self.model.state.in_(states)).order_by(desc(order_by_column)).offset(skip).limit(limit).all()

    def get_multi_by_user(self, db: Session, *, skip: int = 0, limit: int = 0, states: List[str], order_by: str, user_id: int):
        order_by_column = self.order_by_columns.get(order_by)
        if not order_by_column:
            raise INVALID_ORDER_BY_EXCEPTION
        return db.query(self.model).filter(self.model.owner_id == user_id).filter(self.model.state.in_(states)).order_by(desc(order_by_column)).offset(skip).limit(limit).all()

    def create_with_owner(self, db: Session, obj_in: AuctionCreate, owner_id: int) -> Auction:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)  # type: ignore
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
