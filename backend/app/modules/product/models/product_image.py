import sqlalchemy as sa

from app.db.base_class import Base

product_image = sa.Table(
    'product_image', Base.metadata, sa.Column(
        'product_id',
        sa.Integer,
        sa.ForeignKey('product.id')),
    sa. Column(
        'image_id',
        sa.Integer,
        sa.ForeignKey('image.id')))
