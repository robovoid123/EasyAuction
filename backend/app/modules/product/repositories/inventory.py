from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repository.repository_base import BaseRepository

from app.modules.product.schemas import InventoryCreate, InventoryUpdate, InventoryReserveCreate
from app.modules.product.models import Inventory, ServiceType, InventoryReserve

from .inventory_reserve import inventory_reserve_repo

NOT_ENOUGH_PRODUCT_EXCEPTION = HTTPException(status_code=400,
                                             detail="cannot reserve not enough product in inventory")

RESERVE_NOT_FOUND_EXCEPTION = HTTPException(status_code=400,
                                            detail="product is not reserved for the given service")


class InventoryRepository(BaseRepository[Inventory, InventoryCreate,
                                         InventoryUpdate]):

    def increment_quantity(self, db: Session, db_obj: Inventory, quantity: int):
        new_quantity = db_obj.quantity + quantity
        db_obj.quantity = new_quantity
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def decrement_quantity(self, db: Session, db_obj: Inventory, quantity: int):
        if db_obj.quantity < quantity:
            raise NOT_ENOUGH_PRODUCT_EXCEPTION
        new_quantity = db_obj.quantity - quantity
        db_obj.quantity = new_quantity
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_reserve_with_service_type(self, db_obj: Inventory, service_type: ServiceType) -> Optional[InventoryReserve]:
        if db_obj.reserve:
            for r in db_obj.reserve:
                if r.service_type == service_type:
                    return r
        return None

    def create_reserve(self, db: Session, db_obj: Inventory, quantity: int, service_type: ServiceType) -> Inventory:
        # create new inventory reserve
        obj_in = InventoryReserveCreate(
            quantity=quantity,
            service_type=service_type
        )
        inventory_reserve_repo.create_with_inventory(
            db, obj_in=obj_in, inventory_id=db_obj.id)

        self.decrement_quantity(db, db_obj=db_obj, quantity=quantity)

        return db_obj

    def cancel_reserve(self, db: Session, db_obj: Inventory, service_type: ServiceType) -> Inventory:
        reserve = self.get_reserve_with_service_type(
            db_obj=db_obj, service_type=service_type)

        if reserve:
            self.increment_quantity(db, db_obj=db_obj, quantity=reserve.quantity)
            inventory_reserve_repo.remove(db, id=reserve.id)
            return db_obj
        else:
            raise RESERVE_NOT_FOUND_EXCEPTION

    def free_reserve(self, db: Session, db_obj: Inventory, service_type: ServiceType):
        reserve = self.get_reserve_with_service_type(
            db_obj=db_obj, service_type=service_type)
        if reserve:
            inventory_reserve_repo.remove(db, id=reserve.id)
            return db_obj
        else:
            raise RESERVE_NOT_FOUND_EXCEPTION


inventory_repo = InventoryRepository(Inventory)
