from sqlalchemy.orm.session import Session
from sqlalchemy import func, desc
from app.modules.auction.schemas import BidCreate, BidUpdate
from app.modules.auction.models import Bid
from app.repository.repository_base import BaseRepository

from app.modules.auction.models.auction import Auction


class BidRepository(BaseRepository[Bid, BidCreate,
                                   BidUpdate]):
    def get_bidder_auction(self, db: Session, *, skip: int = 0, limit: int = 100, bidder_id: int):
        bid_count = func.count(self.model.auction_id)
        auctions = db.query(self.model.auction_id, bid_count.label("bidder_bid_count")).join(Auction, self.model.auction_id == Auction.id).filter(
            self.model.bidder_id == bidder_id).group_by(self.model.auction_id)
        auctions = auctions.order_by(
            desc(bid_count)).offset(skip).limit(limit).all()
        auctions = [db.query(Auction).get(a.auction_id) for a in auctions]
        return auctions


bid_repo = BidRepository(Bid)
