import uuid
from decimal import Decimal
import enum
from datetime import datetime

from auction_strategy import strategy_factory, AuctionType


class AuctionState(str, enum.Enum):
    CREATED = 'created'
    ENDED = 'ended'
    ONGOING = 'ongoing'
    CANCLED = 'cancled'


class Auction:
    def __init__(self, *,
                 product,
                 starting_bid,
                 bid_cap,
                 strategy=AuctionType.ENGLISH,
                 ending_date):

        self.id = uuid.uuid1()
        self._starting_bid_amount = Decimal(starting_bid)
        self._bid_cap = bid_cap
        self._ending_date = ending_date
        self._strategy = strategy_factory(strategy)

        self._state = AuctionState.CREATED

        self._starting_date = None
        self._current_highest_bid = None
        self._current_winner = None

        self._final_winner = None
        self._winning_bid_amount = None

    def bid_in_auction(self, bid):
        if self.is_auction_ended() and self._state is not AuctionState.CREATED:
            print("invalid auction")
            self.end()
        elif self._state is AuctionState.CREATED:
            print("auction has not started")
        elif self._state is AuctionState.ONGOING:
            self._strategy(self, bid)

    @property
    def current_winner(self):
        return self._current_winner

    @property
    def current_highest_bid(self):
        return self._current_highest_bid

    @property
    def starting_bid_amount(self):
        return self._starting_bid_amount

    def set_current_winning_bid(self, bid):
        self._current_highest_bid = bid
        self._current_winner = bid.bidder

    def is_auction_ended(self):
        return self._ending_date < datetime.now()

    def start(self):
        # record exact time start was run
        self._starting_date = datetime.now()

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
            self._winning_bid = self._current_highest_bid
            self._state = AuctionState.ENDED
        elif self._state is AuctionState.ENDED:
            print("Auction already ended")
        else:
            self._state = AuctionState.CANCLED
