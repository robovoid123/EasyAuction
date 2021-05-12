import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Shop(Base):
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String)
    description = sa.Column(sa.String)

    owner_id = sa.Column(sa.ForeignKey('user.id'))

    products = relationship("PublishedProduct", back_populates="shop")


class BuyHistory(Base):
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    quantity = sa.Column(sa.Integer)
    product_id = sa.Column(sa.ForeignKey('publishedproduct.id'))
    buyer_id = sa.Column(sa.ForeignKey('user.id'))

    product = relationship("PublishedProduct", back_populates="buy_history")


class PublishedProduct(Base):
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    price = sa.Column(sa.Float)
    quantity = sa.Column(sa.Integer)

    product_id = sa.Column(sa.ForeignKey('product.id'))
    shop_id = sa.Column(sa.ForeignKey('shop.id'))

    product = relationship("Product")
    shop = relationship("Shop", back_populates="products")
    buy_history = relationship("BuyHistory", back_populates="product")
