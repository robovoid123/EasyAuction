from app.models.auction import AuctionType
from sqlalchemy.orm import Session
from app.easy_auction.auction import Auction

from app.easy_auction.auction_factory import auction_factory


def test_get_auction(db: Session):
    auction = auction_factory.get_auction(type=AuctionType.ENGLISH)

    assert auction

    auction_methods = dir(auction)

    assert 'bid' in auction_methods
    assert 'start' in auction_methods
    assert 'end' in auction_methods
    assert 'cancel' in auction_methods
    assert 'buy_it_now' in auction_methods


def test_add_auction(db: Session):

    class TestAuction(Auction):
        pass

    auction_factory.add_auction(type="TEST", creator=TestAuction)
    auction = auction_factory.get_auction("TEST")
    auction_methods = dir(auction)

    assert auction
    assert 'bid' in auction_methods
    assert 'start' in auction_methods
    assert 'end' in auction_methods
    assert 'cancel' in auction_methods
    assert 'buy_it_now' in auction_methods
