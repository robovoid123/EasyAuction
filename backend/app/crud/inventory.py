from fastapi.encoder import jsonable_encoder

from app.crud.base import CRUDBase
from app.schemas import product as ps
from app.models.product import Inventory


class CRUDInventory(CRUDBase[Inventory, ps.InventoryCreate, ps.InventoryUpdate]):
    def create_with_date(self, db, obj_in, date):
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, restocked_at=date)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


inventory = CRUDInventory(Inventory)
