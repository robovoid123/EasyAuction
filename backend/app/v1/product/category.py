from sqlalchemy.orm import Session

from app.easy_auction.base import Base
from app.crud.product.category import crud_category


class Category(Base):
    def __init__(self, db: Session):
        super().__init__(crud_category, db)

    def get_with_names(self, names):
        return self.crud.get_with_names(names)
