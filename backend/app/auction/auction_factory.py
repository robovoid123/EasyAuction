from app.models.auction import AuctionType
from app.auction.types import dutch_auction, english_auction
from app.auction.auction import Auction


class AuctionFactory:
    def __init__(self):
        self._auction_creators = {}

    def register_auction(self, type, auction_creator):
        self._auction_creators[type] = auction_creator

    def get_auction(self, type, db, *, crud_auction, crud_auction_session,
                    crud_bid, id=None) -> Auction:
        auction_creator = self._auction_creators.get(type)
        if not auction_creator:
            raise ValueError(type)
        return auction_creator(db, crud_auction, crud_auction_session, crud_bid, id)


factory = AuctionFactory()

factory.register_auction(AuctionType.DUTCH, dutch_auction.DutchAuction)
factory.register_auction(AuctionType.ENGLISH, english_auction.EnglishAuction)
