from app.crud.base import CRUDBase
from app.schemas.product import InventoryCreate, InventoryUpdate
from app.models.product import Inventory


class CRUDInventory(CRUDBase[Inventory, InventoryCreate,
                             InventoryUpdate]):
    pass


crud_inventory = CRUDInventory(Inventory)
