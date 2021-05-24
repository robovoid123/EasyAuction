
from sqlalchemy.orm.session import Session

from sqlalchemy.orm.session import Session
from datetime import datetime, timedelta

from app.schemas.auction import AuctionCreate
from app.models.auction import AuctionType, Auction as AuctionModel
from app.tests.utils.product import create_random_product
from app.tests.utils.utils import random_float
from app.crud.auction.auction import crud_auction


def create_random_auction(db: Session) -> AuctionModel:

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
        bid_cap=bid_cap
    )
    return crud_auction.create_with_owner(db, obj_in=auc_obj,
                                          owner_id=owner_id, ending_date=ending_date)
