import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from .product_category import product_category


class Category(Base):
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String)

    products = relationship(
        'Product', secondary=product_category, back_populates='categories'
    )
