from decimal import DivisionByZero
from app.modules.auction.models.auction_state import AuctionState
from sqlalchemy.orm import Session, session

from app.modules.auction.repositories import auction_repo
from app.modules.auction.auction.english_auction import EnglishAuction
from app.tests.utils.auction import create_random_auction
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_float


def test_start(db: Session):
    auction = create_random_auction(db)

    assert auction.state == AuctionState.CREATED

    english = EnglishAuction()
    english.start(db, db_obj=auction)

    auction = auction_repo.get(db, id=auction.id)
    assert auction.state == AuctionState.ONGOING


def test_bid(db: Session):
    auction = create_random_auction(db)
    english = EnglishAuction()
    english.start(db, db_obj=auction)
    assert auction.state == AuctionState.ONGOING

    amount = auction.starting_amount + 1
    bidder = create_random_user(db)
    english.bid(db, db_obj=auction, amount=amount, bidder_id=bidder.id)

    db_obj = auction_repo.get(db, id=auction.id)
    assert db_obj.current_bid_amount == amount + 1.25
    assert db_obj.last_bid_at
    assert db_obj.winning_bid.amount == amount
    assert db_obj.bids


def test_bid_bid_cap(db: Session):
    auction = create_random_auction(db)
    english = EnglishAuction()
    english.start(db, db_obj=auction)
    assert auction.state == AuctionState.ONGOING

    amount = auction.bid_cap
    bidder = create_random_user(db)
    english.bid(db, db_obj=auction, amount=amount, bidder_id=bidder.id)

    db_obj = auction_repo.get(db, id=auction.id)
    assert db_obj.current_bid_amount == db_obj.bid_cap
    assert db_obj.last_bid_at
    assert db_obj.winning_bid.amount == amount
    assert db_obj.bids
    assert db_obj.state == AuctionState.ENDED
    assert db_obj.final_winner_id == bidder.id


def test_end(db: Session):
    auction = create_random_auction(db)
    english = EnglishAuction()
    english.start(db, db_obj=auction)
    assert auction.state == AuctionState.ONGOING

    amount = auction.reserve + random_float()
    bidder = create_random_user(db)
    english.bid(db, db_obj=auction, amount=amount, bidder_id=bidder.id)
    db_obj = auction_repo.get(db, id=auction.id)

    assert db_obj.winning_bid

    english.end(db, db_obj=db_obj)
    assert db_obj.state == AuctionState.ENDED
    assert db_obj.final_winner_id == bidder.id


def test_end_when_reserve_not_met(db: Session):
    auction = create_random_auction(db)
    english = EnglishAuction()
    english.start(db, db_obj=auction)
    assert auction.state == AuctionState.ONGOING

    amount = auction.current_bid_amount + 2
    bidder = create_random_user(db)
    english.bid(db, db_obj=auction, amount=amount, bidder_id=bidder.id)
    db_obj = auction_repo.get(db, id=auction.id)

    assert db_obj.winning_bid

    english.end(db, db_obj=db_obj)
    assert db_obj.state == AuctionState.CANCLED
    assert not db_obj.final_winner_id


def test_cancel(db: Session):
    auction = create_random_auction(db)
    english = EnglishAuction()
    english.start(db, db_obj=auction)
    assert auction.state == AuctionState.ONGOING

    amount = auction.starting_amount + random_float()
    bidder = create_random_user(db)
    english.bid(db, db_obj=auction, amount=amount, bidder_id=bidder.id)
    db_obj = auction_repo.get(db, id=auction.id)

    assert db_obj.winning_bid

    english.cancel(db, db_obj=db_obj)
    assert db_obj.state == AuctionState.CANCLED
    assert not db_obj.final_winner_id


def test_buy_it_now(db: Session):
    auction = create_random_auction(db)
    english = EnglishAuction()
    english.start(db, db_obj=auction)
    assert auction.state == AuctionState.ONGOING

    buyer = create_random_user(db)
    english.buy_it_now(db, db_obj=auction, buyer_id=buyer.id)
    db_obj = auction_repo.get(db, id=auction.id)

    assert db_obj.state == AuctionState.ENDED
    assert db_obj.current_bid_amount == db_obj.bid_cap
    assert db_obj.final_winner_id == buyer.id
