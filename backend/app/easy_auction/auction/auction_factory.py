from app.models.auction import AuctionType
from app.easy_auction.auction.types import dutch_auction, english_auction
from app.easy_auction.auction.auction import Auction


class AuctionFactory:
    def __init__(self):
        self._auction_creators = {}

    def register_auction(self, au_type, auction_creator):
        self._auction_creators[au_type] = auction_creator

    def get_auction(self, au_type, db, id=None, db_obj=None) -> Auction:
        auction_creator = self._auction_creators.get(au_type)
        if not auction_creator:
            raise ValueError(au_type)
        if id:
            return auction_creator(db, id=id)
        if db_obj:
            return auction_creator(db, db_obj=db_obj)

    def get_new_auction(self, au_type, db, obj_in, owner_id) -> Auction:
        auction_creator = self._auction_creators.get(au_type)
        if not auction_creator:
            raise ValueError(au_type)
        return auction_creator.create(db, obj_in, owner_id)


factory = AuctionFactory()

factory.register_auction(AuctionType.DUTCH, dutch_auction.DutchAuction)
factory.register_auction(AuctionType.ENGLISH, english_auction.EnglishAuction)
