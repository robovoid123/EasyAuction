from app.modules.auction.models.auction_state import AuctionState
from sqlalchemy.orm.session import Session

from app.modules.auction.schemas import AuctionCreate
from app.tests.utils.product import create_random_product
from app.tests.utils.utils import random_float
from app.modules.auction.repositories import auction_repo


def test_create_auction(db: Session):
    product = create_random_product(db)
    starting_amount = random_float()
    reserve = starting_amount + random_float()
    bid_cap = reserve + random_float()
    owner = product.owner

    auction = auction_repo.create(db, obj_in=AuctionCreate(
        product_id=product.id,
        owner_id=owner.id,
        starting_amount=starting_amount,
        reserve=reserve,
        bid_cap=bid_cap
    ))

    db_obj = auction_repo.get(db, id=auction.id)

    assert db_obj
    assert db_obj.product_id == product.id
    assert db_obj.owner_id == owner.id
    assert db_obj.starting_amount == starting_amount
    assert db_obj.reserve == reserve
    assert db_obj.bid_cap == bid_cap
    assert db_obj.state == AuctionState.CREATED


def test_update_auction(db: Session): pass
def test_delete_auction(db: Session): pass
def test_update_with_date(db: Session): pass
