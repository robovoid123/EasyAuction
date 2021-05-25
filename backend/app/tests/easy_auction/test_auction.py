from app.models.auction import AuctionState
from sqlalchemy.orm.session import Session

from app.tests.utils.auction import create_random_auction
from app.tests.utils.user import create_random_user
from app.easy_auction.auction_factory import auction_factory
from app.crud.auction.auction import crud_auction


def test_cancel_auction(db: Session):
    auction_db = create_random_auction(db)

    auction = auction_factory.get_auction(type=auction_db.au_type)
    assert auction

    auction.start(db, id=auction_db.id)
    auction_db = crud_auction.get(db, auction_db.id)
    assert auction_db.session
    assert auction_db.session.state == AuctionState.ONGOING
    assert not auction_db.is_ended

    auction.cancel(db, auction_db.id)
    auction_db = crud_auction.get(db, auction_db.id)
    assert auction_db.session.state == AuctionState.CANCLED
    assert auction_db.is_ended == True


def test_bid_reserve_not_reached(db: Session):
    auction_db = create_random_auction(db)

    auction = auction_factory.get_auction(type=auction_db.au_type)
    assert auction

    auction.start(db, id=auction_db.id)
    auction_db = crud_auction.get(db, auction_db.id)
    assert auction_db.session
    assert auction_db.session.state == AuctionState.ONGOING

    amount = auction_db.reserve - 1
    bidder = create_random_user(db)
    auction.bid(db, id=auction_db.id, amount=amount, bidder_id=bidder.id)

    auction_db = crud_auction.get(db, id=auction_db.id)
    assert auction_db.session.winning_bid
    winning_bid = auction_db.session.winning_bid
    assert winning_bid.amount == amount
    assert winning_bid.bidder_id == bidder.id
    assert auction_db.session.last_bid_at
    assert auction_db.session.bid_line == amount + 1.25
    assert auction_db.session.state == AuctionState.ONGOING

    auction.end(db, id=auction_db.id)
    auction_db = crud_auction.get(db, id=auction_db.id)
    assert not auction_db.final_cost
    assert not auction_db.winner_id
    assert auction_db.is_ended
    assert auction_db.session.state == AuctionState.ENDED


def test_bid_bid_cap_reached(db: Session):
    auction_db = create_random_auction(db)

    auction = auction_factory.get_auction(type=auction_db.au_type)
    assert auction

    auction.start(db, id=auction_db.id)
    auction_db = crud_auction.get(db, auction_db.id)
    assert auction_db.session
    assert auction_db.session.state == AuctionState.ONGOING

    amount = auction_db.bid_cap + 1
    bidder = create_random_user(db)
    auction.bid(db, id=auction_db.id, amount=amount, bidder_id=bidder.id)

    auction_db = crud_auction.get(db, id=auction_db.id)
    assert auction_db.session.winning_bid
    winning_bid = auction_db.session.winning_bid
    assert winning_bid.amount == amount
    assert winning_bid.bidder_id == bidder.id
    assert auction_db.session.last_bid_at
    assert auction_db.session.bid_line == auction_db.bid_cap
    assert auction_db.session.state == AuctionState.ENDED


def test_bid_less_then_bid_line(db: Session):
    pass
