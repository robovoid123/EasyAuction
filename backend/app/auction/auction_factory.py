from app.models.auction import AuctionType
from app.auction.types import dutch_auction, english_auction
from app.auction.auction import Auction


class AuctionFactory:
    def __init__(self):
        self._auction_creators = {}

    def register_auction(self, au_type, auction_creator):
        self._auction_creators[au_type] = auction_creator

    def get_auction(self, au_type, db, id=None) -> Auction:
        auction_creator = self._auction_creators.get(au_type)
        if not auction_creator:
            raise ValueError(au_type)
        return auction_creator(db, id)


factory = AuctionFactory()

factory.register_auction(AuctionType.DUTCH, dutch_auction.DutchAuction)
factory.register_auction(AuctionType.ENGLISH, english_auction.EnglishAuction)
