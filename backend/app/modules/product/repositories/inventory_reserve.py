from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.repository.repository_base import BaseRepository

from app.modules.product.schemas import InventoryReserveCreate, InventoryReserveUpdate
from app.modules.product.models import InventoryReserve


class InventoryReserveRepository(BaseRepository[InventoryReserve, InventoryReserveCreate,
                                                InventoryReserveUpdate]):
    def create_with_inventory(self, db: Session, *, obj_in: InventoryReserveCreate, inventory_id: int):
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, inventory_id=inventory_id)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


inventory_reserve_repo = InventoryReserveRepository(InventoryReserve)
