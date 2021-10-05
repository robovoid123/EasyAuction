from re import S
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from .bid import Bid
from .auction_state import AuctionState


class Auction(Base):
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    starting_amount = sa.Column(sa.Float, nullable=False)
    bid_cap = sa.Column(sa.Float)  # max amount bidder can bid
    reserve = sa.Column(sa.Float)  # final amount must be >= reserve

    state = sa.Column(sa.String, index=True, default=AuctionState.CREATED.value)
    current_bid_amount = sa.Column(sa.Float)
    last_bid_at = sa.Column(sa.DateTime)
    bid_count = sa.Column(sa.Integer, default=0)

    ending_date = sa.Column(sa.DateTime)  # for scheduler to end auction
    starting_date = sa.Column(sa.DateTime)  # for scheduler to start auction

    winning_bid_id = sa.Column(sa.ForeignKey('bid.id'))
    owner_id = sa.Column(sa.ForeignKey('user.id'))
    product_id = sa.Column(sa.ForeignKey('product.id'))
    final_winner_id = sa.Column(sa.ForeignKey('user.id'))

    winning_bid = relationship('Bid', foreign_keys=[winning_bid_id])
    product = relationship("Product")
    owner = relationship("User", foreign_keys=[owner_id])
    final_winner = relationship("User", foreign_keys=[final_winner_id])
    bids = relationship('Bid', foreign_keys=[Bid.auction_id], back_populates='auction')
