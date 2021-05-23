from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.easy_auction.base import Base
from app.crud.product.inventory import crud_inventory


class Inventory(Base):
    def __init__(self, db: Session):
        super().__init__(crud_inventory, db)

    def reserve(self, db_obj, quantity):
        if db_obj.quantity < quantity:
            raise HTTPException(
                status_code=400,
                detail="cannot reserve not enough product in inventory"
            )
        self.update(db_obj, {'quantity': db_obj.quantity - quantity})
        return db_obj

    def free(self, db_obj, quantity):
        self.update(db_obj, {'quantity': db_obj.quantity + quantity})
        return db_obj
