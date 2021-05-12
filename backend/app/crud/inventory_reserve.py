from app.crud.base import CRUDBase
from app.schemas.product import (
    InventoryReserveCreate,
    InventoryReserveUpdate
)
from app.models.product import InventoryReserve


class CRUDInventoryReserve(CRUDBase[InventoryReserve, InventoryReserveCreate,
                                    InventoryReserveUpdate]):
    pass


incentory_reserve = CRUDInventoryReserve(InventoryReserve)
