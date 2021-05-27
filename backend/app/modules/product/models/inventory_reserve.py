import sqlalchemy as sa

from app.db.base_class import Base
from .service_type import ServiceType


class InventoryReserve(Base):
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    quantity = sa.Column(sa.Integer)
    service_type = sa.Column(sa.Enum(ServiceType))
    created_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())

    inventory_id = sa.Column(sa.ForeignKey('inventory.id'))
