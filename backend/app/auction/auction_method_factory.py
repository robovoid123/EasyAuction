from app.models.auction import AuctionType
from app.auction.auction_methods.english_auction import EnglishAuction
from app.auction.auction_methods.dutch_auction import DutchAuction


class AuctionMethodFactory:

    def get_method(self, type: AuctionType):

        if type == AuctionType.ENGLISH:

            return EnglishAuction()

        elif type == AuctionType.DUTCH:

            return DutchAuction()

        else:

            raise ValueError(type)


auction_method_factory = AuctionMethodFactory()
