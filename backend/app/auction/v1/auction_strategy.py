import enum


class AuctionType(str, enum.Enum):
    ENGLISH = 'english'
    DUTCH = 'dutch'


def english_auction(auction, amount, bidder):
    if not auction.current_highest_bid:
        if amount > auction.starting_bid_amount:
            auction.set_current_winning_bid(amount, bidder)
        else:
            print("bid must be higer than starting bid")
    elif amount > auction.current_highest_bid.amount:
        auction.set_current_winning_bid(amount, bidder)
    else:
        print('bid too low')


def dutch_auction(auction, bid):
    pass


def strategy_factory(strategy_name):
    if strategy_name == AuctionType.ENGLISH:
        return english_auction
    elif strategy_name == AuctionType.DUTCH:
        return dutch_auction
    else:
        raise ValueError(strategy_name)
