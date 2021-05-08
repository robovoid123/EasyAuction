from typing import Optional
import json
import uuid
from decimal import Decimal
from datetime import datetime

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from app.auction.redis import redis
from app.db.session import SessionLocal
from app.models.auction import Auction as AuctionM
from app.auction.auction_strategy import strategy_factory, AuctionType


CREATED = 'created'
ENDED = 'ended'
ONGOING = 'ongoing'
CANCLED = 'cancled'


class Bid(BaseModel):
    id: uuid.UUID
    amount: float


class AuctionS(BaseModel):
    id: Optional[int]
    product_id: str
    starting_bid_amount: float
    auction_type: AuctionType
    bid_cap: Optional[float]
    reserve: Optional[float]
    ending_date: datetime
    state: Optional[str]
    starting_date: Optional[datetime]
    current_highest_bid: Optional[float]
    current_winner: Optional[int]
    final_winner: Optional[int]
    winning_bid_amount: Optional[float]


class Auction:
    def __init__(self, *,
                 product_id,
                 starting_bid_amount,
                 bid_cap,
                 reserve,
                 auction_type,
                 ending_date):

        self.id = None
        self.product_id = product_id
        self.starting_bid_amount = Decimal(starting_bid_amount)
        self.bid_cap = bid_cap
        self.reserve = reserve
        self.ending_date = ending_date
        self.auction_type = auction_type or AuctionType.ENGLISH
        self._strategy = strategy_factory(self.auction_type)

        self.state = CREATED

        self.starting_date = None
        self.current_highest_bid = None
        self.current_winner = None

        self.final_winner = None
        self.winning_bid_amount = None

    @classmethod
    def load_from_dict(cls, data):
        auction = cls(
            product=data.get('product'),
            starting_bid_amount=data.get('starting_bid_amount'),
            bid_cap=data.get('bid_cap'),
            reserve=data.get('reserve'),
            auction_type=data.get('auction_type'),
            ending_date=datetime.fromisoformat(data.get('ending_date'))
        )
        auction.id = data.get('id')
        auction.starting_date = data.get('starting_date')
        auction.current_highest_bid = data.get('current_highest_bid')
        auction.current_winner = data.get('current_winner')
        auction.final_winner = data.get('final_winner')
        auction.winning_bid_amount = data.get('winning_bid_amount')
        auction.state = data.get('state')
        return auction

    def store_in_redis(self):
        auction_id = f'auction_{self.id}'
        redis.set(auction_id, json.dumps(self.serialize()))

    def store_in_db(self):
        with SessionLocal() as db:
            auction = AuctionM(**self.serialize())
            db.add(auction)
            db.commit()
            db.refresh(auction)
            return auction

    def bid_in_auction(self, amount, bidder):
        if self.is_auction_ended() and self.state != CREATED:
            print("invalid auction")
            self.end()
        elif self.state == CREATED:
            print("auction has not started")
        elif self.state == ONGOING:
            self._strategy(self, amount, bidder)
        else:
            raise ValueError(self.state)

    def serialize(self):
        return AuctionS(**jsonable_encoder(self)).dict()

    def set_current_winning_bid(self, amount, bidder):
        self.current_highest_bid = amount
        self.current_winner = bidder

    def is_auction_ended(self):
        return self.ending_date < datetime.now() or self.state == ENDED

    def start(self):
        self.starting_date = datetime.now()

        if self.state is ONGOING:
            print("auction already started")
        elif self.state is ENDED:
            print("auction already ended")
        elif self.state is CANCLED:
            print("auction canceled")
        else:
            self.state = ONGOING

    def end(self):
        if self.current_winner and self.state is ONGOING:
            self.final_winner = self.current_winner
            self.winning_bid = self.current_highest_bid
            self.state = ENDED
        elif self.state is ENDED:
            print("Auction already ended")
        else:
            self.state = CANCLED
