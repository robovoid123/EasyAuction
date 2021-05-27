from typing import Optional

from pydantic import BaseModel
from app.modules.product.models.service_type import ServiceType


class InventoryReserveBase(BaseModel):
    quantity: Optional[int]
    service_type: Optional[ServiceType]


class InventoryReserveCreate(InventoryReserveBase):
    quantity: int
    service_type: ServiceType


class InventoryReserveUpdate(InventoryReserveBase):
    pass
