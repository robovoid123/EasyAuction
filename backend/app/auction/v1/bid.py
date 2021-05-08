from decimal import Decimal


class Bid:
    def __init__(self, amount, user_id, auction):
        self.amount = Decimal(amount)
        self.bidder = user_id
        self.auction = auction

        self.auction.bid_in_auction(self.amount, self.bidder)

    def __repr__(self):
        return f'Bid(amount={self.amount}, bidder={self.bidder})'

    def store_in_db(self):
        pass
