import uuid
import enum
from datetime import datetime


class AuctionState(str, enum.Enum):
    CREATED = 'created'
    ENDED = 'ended'
    ONGOING = 'ongoing'
    CANCLED = 'cancled'


VALIDSTATE = [AuctionState.CREATED, AuctionState.ONGOING]


def english_auction(auction, bid):
    if auction.current_highest_bid is None\
        and bid.amount > auction._starting_bid\
            or bid.amount > auction.current_highest_bid.amount:
        auction.current_highest_bid = bid
        auction.current_winner = bid.bidder
    else:
        print('bid too low')


def dutch_auction(auction, bid):
    pass


def fpsb(auction, bid):
    pass


def spsb(auction, bid):
    pass


def strategy_factory(strategy_name):
    if strategy_name == "english":
        return english_auction
    elif strategy_name == "dutch":
        return dutch_auction
    else:
        raise ValueError(strategy_name)


class Auction:
    def __init__(self, *,
                 product,
                 starting_bid,
                 bid_cap,
                 starting_date=None,
                 strategy=english_auction,
                 ending_date):
        self.id = uuid.uuid1()
        self._starting_bid = starting_bid
        self._current_highest_bid = None
        self._bid_cap = bid_cap
        self._ending_date = ending_date
        self._starting_date = starting_date or datetime.now()
        self._state = AuctionState.CREATED
        self._current_winner = None
        self._strategy = strategy

        self._final_winner = None
        self._winning_bid_amount = None

    def strategy(self, bid):
        if not self.is_valid():
            self.end()
            return
        return self._strategy(self, bid)

    @property
    def current_winner(self):
        return self._current_winner

    @current_winner.setter
    def current_winner(self, user_id):
        self._current_winner = user_id

    @property
    def current_highest_bid(self):
        return self._current_highest_bid

    @current_highest_bid.setter
    def current_highest_bid(self, bid):
        self._current_highest_bid = bid

    def is_valid(self):
        return self._ending_date > datetime.now()

    def start(self):
        if self._state is AuctionState.ONGOING:
            print("auction already started")
        elif self._state is AuctionState.ENDED:
            print("auction already ended")
        elif self._state is AuctionState.CANCLED:
            print("auction canceled")
        else:
            self._state = AuctionState.ONGOING

    def end(self):
        if self._current_winner and self._state is AuctionState.ONGOING:
            self._final_winner = self._current_winner
            self._winning_bid_amount = self._current_highest_bid
            self._state = AuctionState.ENDED
        elif self._state is AuctionState.ENDED:
            print("Auction already ended")
        else:
            self._state = AuctionState.CANCLED
