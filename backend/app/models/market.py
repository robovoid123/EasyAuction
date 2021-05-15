import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.db.base_class import Base

product_shop = sa.Table(
    'product_shop', Base.metadata, sa.Column(
        'product_id',
        sa.Integer,
        sa.ForeignKey('publishedproduct.id')),
    sa.Column(
        'shop_id',
        sa.Integer,
        sa.ForeignKey('shop.id')))


class Shop(Base):
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String)
    description = sa.Column(sa.String)

    owner_id = sa.Column(sa.ForeignKey('user.id'))

    products = relationship(
        "PublishedProduct", secondary=product_shop, back_populates="shop")


class PublishedProductLog(Base):
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    quantity = sa.Column(sa.Integer)

    product_id = sa.Column(sa.ForeignKey('publishedproduct.id'))
    buyer_id = sa.Column(sa.ForeignKey('user.id'))

    product = relationship("PublishedProduct", back_populates="log")


class PublishedProduct(Base):
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    price = sa.Column(sa.Float)
    quantity = sa.Column(sa.Integer)

    product_id = sa.Column(sa.ForeignKey('product.id'))

    product = relationship("Product")
    shop = relationship("Shop", secondary=product_shop, back_populates="products")
    log = relationship("BuyHistory", back_populates="product")
