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


class Auction(Base):
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    starting_bid_amount = sa.Column(sa.Float)
    bid_cap = sa.Column(sa.Float)
    reserve = sa.Column(sa.Float)
    ending_date = sa.Column(sa.DateTime)
    starting_date = sa.Column(sa.DateTime)
    type = sa.Column(sa.Enum(AuctionType))
    final_cost = sa.Column(sa.Float)
    is_ended = sa.Column(sa.Boolean, default=0)

    owner_id = sa.Column(sa.ForeignKey('user.id'))
    product_id = sa.Column(sa.ForeignKey('product.id'))
    winner_id = sa.Column(sa.ForeignKey('user.id'))

    products = relationship("Product")
    owner = relationship("User", foreign_keys=[owner_id])
    winner = relationship("User", foreign_keys=[winner_id])
    auction_session = relationship(
        "AuctionSession", uselist=False, back_populates='auction')


auction_bid = sa.Table(
    'auction_bid', Base.metadata, sa.Column(
        'auction_session_id',
        sa.Integer,
        sa.ForeignKey('auctionsession.id')),
    sa.Column(
        'bid_id',
        sa.Integer,
        sa.ForeignKey('bid.id')))


class Bid(Base):
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    amount = sa.Column(sa.Float)
    created_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())

    bidder_id = sa.Column(sa.ForeignKey('user.id'))

    auction_session = relationship(
        'AuctionSession', secondary=auction_bid, back_populates='bids')


class AuctionSession(Base):
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    state = sa.Column(sa.String)
    # bid should be higher than bid line in English auction
    bid_line = sa.Column(sa.Float)
    last_bid_at = sa.Column(sa.DateTime)

    current_highest_bid_id = sa.Column(sa.ForeignKey('bid.id'))
    auction_id = sa.Column(sa.ForeignKey('auction.id'))

    auction = relationship('Auction', back_populates='auction_session')
    current_highest_bid = relationship('Bid', foreign_keys=[current_highest_bid_id])
    bids = relationship('Bid', secondary=auction_bid,
                        back_populates='auction_session')
