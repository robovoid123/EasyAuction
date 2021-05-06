import enum


class AuctionType(str, enum.Enum):
    ENGLISH = 'english'
    DUTCH = 'dutch'


def english_auction(auction, bid):
    if not auction.current_highest_bid:
        if bid.amount > auction.starting_bid_amount:
            auction.set_current_winning_bid(bid)
        else:
            print("bid must be higer than starting bid")
    elif bid.amount > auction.current_highest_bid.amount:
        auction.set_current_winning_bid(bid)
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
