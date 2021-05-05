class Bid:
    def __init__(self, amount, user_id, auction):
        self.amount = amount
        self.bidder = user_id
        self.auction = auction

        self.auction.strategy(self)
