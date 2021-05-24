from app.models.auction import AuctionState
from sqlalchemy.orm.session import Session

from app.tests.utils.auction import create_random_auction
from app.easy_auction.auction_factory import auction_factory
from app.crud.auction.auction import crud_auction


def test_cancel_auction(db: Session):
    auction_db = create_random_auction(db)

    auction = auction_factory.get_auction(type=auction_db.au_type)
    assert auction

    auction.start(db, id=auction_db.id)
    auction_db = crud_auction.get(db, auction_db.id)
    assert auction_db.session
    print(auction_db.session)
    assert auction_db.session.state == AuctionState.ONGOING
    assert not auction_db.is_ended

    auction.cancel(db, auction_db.id)
    auction_db = crud_auction.get(db, auction_db.id)
    assert auction_db.session.state == AuctionState.CANCLED
    assert auction_db.is_ended == True
