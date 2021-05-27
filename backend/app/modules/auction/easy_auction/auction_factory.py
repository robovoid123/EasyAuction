from app.models.auction import AuctionType
from app.easy_auction.auction import Auction
from app.easy_auction.variation.english_auction import EnglishAuction


class AuctionFactory:
    creators = {}

    @classmethod
    def get_auction(cls, type: AuctionType) -> Auction:
        if AuctionFactory.creators.get(type):
            return AuctionFactory.creators.get(type)()
        else:
            raise ValueError(type)

    @classmethod
    def add_auction(cls, type: AuctionType, creator) -> None:
        if AuctionFactory.creators.get(type):
            raise Exception("auction type already added")
        else:
            AuctionFactory.creators[type] = creator


auction_factory = AuctionFactory()

auction_factory.add_auction(AuctionType.ENGLISH, EnglishAuction)
