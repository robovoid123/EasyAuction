from enum import auto
from sqlalchemy.orm.session import Session
from datetime import datetime, timedelta

from app.schemas.auction import AuctionCreate, AuctionUpdate
from app.models.auction import AuctionType
from app.tests.utils.product import create_random_product
from app.tests.utils.utils import random_float
from app.crud.auction.auction import crud_auction
from app.tests.utils.auction import create_random_auction


def test_create_with_owner(db: Session):
    prod_db = create_random_product(db)
    starting_bid_amount = random_float()
    reserve = starting_bid_amount + random_float()
    bid_cap = reserve + random_float()
    ending_date = datetime.now() + timedelta(days=2)
    au_type = AuctionType.ENGLISH
    owner_id = prod_db.owner_id

    auc_obj = AuctionCreate(
        product_id=prod_db.id,
        starting_bid_amount=starting_bid_amount,
        au_type=au_type,
        reserve=reserve,
        bid_cap=bid_cap)
    auc_db = crud_auction.create_with_owner(db, obj_in=auc_obj,
                                            owner_id=owner_id, ending_date=ending_date)

    db_obj = crud_auction.get(db, auc_db.id)

    assert db_obj
    assert db_obj == auc_db
    assert db_obj.product_id == prod_db.id
    assert db_obj.starting_bid_amount == starting_bid_amount
    assert db_obj.reserve == reserve
    assert db_obj.bid_cap == bid_cap
    assert db_obj.ending_date == ending_date
    assert db_obj.owner_id == owner_id
    assert db_obj.au_type == au_type


def test_create_auction_with_ending_date_less_then_now(db: Session):
    pass


def test_create_auction_with_bid_cap_less_then_starting_bid_amt(db: Session):
    pass


def test_create_auction_with_reserve_greater_than_bid_cap(db: Session):
    pass


def test_create_auction_with_reserve_less_than_starting_bid_amt(db: Session):
    pass


def test_get_auction(db: Session):
    auction_db = create_random_auction(db)

    db_obj = crud_auction.get(db, auction_db.id)

    assert db_obj
    assert db_obj.owner_id == auction_db.owner_id
    assert db_obj.product_id == auction_db.product_id
    assert db_obj.starting_bid_amount == auction_db.starting_bid_amount
    assert db_obj.reserve == auction_db.reserve
    assert db_obj.bid_cap == auction_db.bid_cap
    assert db_obj.ending_date == auction_db.ending_date
    assert db_obj.au_type == auction_db.au_type


def test_update_auction(db: Session):
    auction_db = create_random_auction(db)

    starting_bid_amount = random_float()
    reserve = starting_bid_amount + random_float()
    bid_cap = reserve + random_float()
    ending_date = datetime.now() + timedelta(days=2)
    au_type = AuctionType.DUTCH

    update_obj = AuctionUpdate(
        starting_bid_amount=starting_bid_amount,
        au_type=au_type,
        reserve=reserve,
        bid_cap=bid_cap)

    crud_auction.update_with_date(
        db, db_obj=auction_db, obj_in=update_obj, ending_date=ending_date)

    db_obj = crud_auction.get(db, auction_db.id)

    assert db_obj
    assert db_obj.owner_id == auction_db.owner_id
    assert db_obj.product_id == auction_db.product_id
    assert db_obj.starting_bid_amount == starting_bid_amount
    assert db_obj.reserve == reserve
    assert db_obj.bid_cap == bid_cap
    assert db_obj.ending_date == ending_date
    assert db_obj.au_type == au_type


def test_delete_auction(db: Session):
    pass
