import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from .conditons import Conditions
from .product_category import product_category


class Product(Base):
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String)
    description = sa.Column(sa.String)
    condition = sa.Column(sa.Enum(Conditions))
    created_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())
    updated_at = sa.Column(sa.DateTime(timezone=True),
                           server_default=sa.func.now(), onupdate=sa.func.now())

    owner_id = sa.Column(sa.ForeignKey('user.id'))
    inventory_id = sa.Column(sa.ForeignKey('inventory.id'))

    owner = relationship("User")
    inventory = relationship("Inventory", back_populates='product')
    categories = relationship(
        'Category', secondary=product_category, back_populates='products')
