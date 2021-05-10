import enum
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Conditions(str, enum.Enum):
    BRAND_NEW = 'brandnew'
    BEST = 'best'
    GOOD = 'good'
    POOR = 'poor'


product_category = sa.Table(
    'product_category', Base.metadata, sa.Column(
        'product_id',
        sa.Integer,
        sa.ForeignKey('product.id')),
    sa. Column(
        'category_id',
        sa.Integer,
        sa.ForeignKey('category.id')))


class Category(Base):
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String)

    products = relationship(
        'Product', secondary=product_category, back_populates='categories'
    )


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


class Inventory(Base):
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    quantity = sa.Column(sa.Integer, default=1)
    restocked_at = sa.Column(sa.DateTime)

    product = relationship('Product', back_populates='inventory')
