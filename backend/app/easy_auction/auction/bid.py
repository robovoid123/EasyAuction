from sqlalchemy.orm import Session

from app.easy_auction.base import Base
from app.crud.auction.bid import crud_bid


class Bid(Base):
    def __init__(self, db: Session):
        super().__init__(crud_bid, db)
