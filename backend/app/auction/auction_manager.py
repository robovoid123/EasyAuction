from auction import Auction, strategy_factory
from bid import Bid


class AuctionManager:
    _auctions = {}

    @classmethod
    def create_auction(cls, *, product,
                       starting_bid, starting_date=None, ending_date, strategy):
        strategy = strategy_factory(strategy)
        new_auction = Auction(product=product,
                              starting_bid=starting_bid,
                              starting_date=starting_date,
                              ending_date=ending_date,
                              strategy=strategy
                              )
        if not cls._auctions.get(new_auction.id):
            cls._auctions[new_auction.id] = new_auction
        return new_auction

    @classmethod
    def start_auction(cls, auction_id):
        auction = cls.get_auction(auction_id)
        if auction:
            auction.start()

    @classmethod
    def bid_in_auction(cls, *, user_id, auction_id, amount):
        auction = cls.get_auction(auction_id)
        if auction:
            bid = Bid(amount=amount, user_id=user_id, auction=auction)
            return bid

    @classmethod
    def get_auction(cls, id):
        if not cls._auctions.get(id):
            # search in db
            pass
        else:
            return cls._auctions[id]


auction_manager = AuctionManager()
