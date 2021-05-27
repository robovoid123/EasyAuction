import sqlalchemy as sa

from app.db.base_class import Base

product_category = sa.Table(
    'product_category', Base.metadata, sa.Column(
        'product_id',
        sa.Integer,
        sa.ForeignKey('product.id')),
    sa. Column(
        'category_id',
        sa.Integer,
        sa.ForeignKey('category.id')))
