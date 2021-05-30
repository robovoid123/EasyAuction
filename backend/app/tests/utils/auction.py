from sqlalchemy.orm.session import Session

from sqlalchemy.orm.session import Session

from app.modules.auction.schemas.auction import AuctionCreate
from app.modules.auction.models.auction import Auction
from app.tests.utils.product import create_random_product
from app.tests.utils.utils import random_float
from app.modules.auction.repositories import auction_repo


def create_random_auction(db: Session) -> Auction:

    product = create_random_product(db)
    starting_amount = random_float()
    reserve = starting_amount + random_float() + 2
    bid_cap = reserve + random_float() + 2
    owner = product.owner

    return auction_repo.create(db, obj_in=AuctionCreate(
        product_id=product.id,
        owner_id=owner.id,
        starting_amount=starting_amount,
        reserve=reserve,
        bid_cap=bid_cap
    ))
