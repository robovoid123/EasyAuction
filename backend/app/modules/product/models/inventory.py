import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Inventory(Base):
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    quantity = sa.Column(sa.Integer)
    updated_at = sa.Column(sa.DateTime(timezone=True),
                           server_default=sa.func.now(), onupdate=sa.func.now())

    product = relationship('Product', back_populates='inventory')
    reserve = relationship('InventoryReserve')
