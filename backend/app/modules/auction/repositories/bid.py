from app.modules.auction.schemas import BidCreate, BidUpdate
from app.modules.auction.models import Bid
from app.repository.repository_base import BaseRepository


class BidRepository(BaseRepository[Bid, BidCreate,
                                   BidUpdate]):
    pass


bid_repo = BidRepository(Bid)
