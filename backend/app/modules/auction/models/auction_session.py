import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from .bid import Bid


class AuctionSession(Base):
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    state = sa.Column(sa.String)  # to track the state
    bid_line = sa.Column(sa.Float)  # bid line represent the max/min user can bid
    bid_cap = sa.Column(sa.Float)  # if bid cap set then auction has limit
    reserve = sa.Column(sa.Float)  # if reserve set then final price must be > reserve
    last_bid_at = sa.Column(sa.DateTime)

    winning_bid_id = sa.Column(sa.ForeignKey('bid.id'))
    auction_id = sa.Column(sa.ForeignKey('auction.id'))

    auction = relationship('Auction', back_populates='session')
    winning_bid = relationship('Bid', foreign_keys=[winning_bid_id])
    bids = relationship('Bid', foreign_keys=[
                        Bid.session_id], back_populates='auction_session')
