import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Bid(Base):
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    amount = sa.Column(sa.Float)
    created_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())

    session_id = sa.Column(sa.ForeignKey('auctionsession.id'))
    bidder_id = sa.Column(sa.ForeignKey('user.id'))

    auction_session = relationship(
        'AuctionSession', foreign_keys=[session_id], back_populates='bids')
