import enum
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class AuctionState(str, enum.Enum):
    ONGOING = 'ongoing'
    ENDED = 'ended'
    CANCLED = 'cancled'


class AuctionType(str, enum.Enum):
    ENGLISH = 'english'
    DUTCH = 'dutch'
    BLIND = 'blind'
    SILENT = 'silent'


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
    session = relationship("AuctionSession", back_populates="auction")


class Bid(Base):
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    amount = sa.Column(sa.Float)
    created_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())

    session_id = sa.Column(sa.ForeignKey('auctionsession.id'))
    bidder_id = sa.Column(sa.ForeignKey('user.id'))

    auction_session = relationship(
        'AuctionSession', foreign_keys=[session_id], back_populates='bids')


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
