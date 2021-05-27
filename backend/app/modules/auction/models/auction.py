import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from .auction_type import AuctionType


class Auction(Base):
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    starting_bid_amount = sa.Column(sa.Float)
    bid_cap = sa.Column(sa.Float)
    reserve = sa.Column(sa.Float)
    ending_date = sa.Column(sa.DateTime)
    starting_date = sa.Column(sa.DateTime)
    au_type = sa.Column(sa.Enum(AuctionType))
    final_cost = sa.Column(sa.Float)
    is_ended = sa.Column(sa.Boolean, default=0)

    owner_id = sa.Column(sa.ForeignKey('user.id'))
    product_id = sa.Column(sa.ForeignKey('product.id'))
    winner_id = sa.Column(sa.ForeignKey('user.id'))

    product = relationship("Product")
    owner = relationship("User", foreign_keys=[owner_id])
    winner = relationship("User", foreign_keys=[winner_id])
    session = relationship("AuctionSession", uselist=False, back_populates="auction")
