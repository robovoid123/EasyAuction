from auction import Auction
from auction_strategy import AuctionType
from bid import Bid


class AuctionManager:
    _auctions = {}

    @classmethod
    def create_auction(cls, *, product,
                       starting_bid,
                       bid_cap=None,
                       reserve=None,
                       starting_date=None,
                       ending_date,
                       auction_type: AuctionType = AuctionType.ENGLISH):
        new_auction = Auction(product=product,
                              starting_bid=starting_bid,
                              bid_cap=bid_cap,
                              starting_date=starting_date,
                              ending_date=ending_date,
                              strategy=auction_type
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

if __name__ == '__main__':
    import datetime
    ending_date = datetime.datetime.now() + datetime.timedelta(seconds=30)
    auction = auction_manager.create_auction(product="apple",
                                             starting_bid=100,
                                             ending_date=ending_date)
    auction.start()

    while True:
        amt = input("bid amount: ")
        user = input("user: ")
        auction_manager.bid_in_auction(user_id=user, auction_id=auction.id, amount=amt)
        print("current bid: ", auction.current_highest_bid)
        print("current winner: ", auction.current_winner)
