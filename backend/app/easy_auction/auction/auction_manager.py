from app.crud.auction import auction as auction_crud

from app.easy_auction.auction.auction_factory import factory
from app.easy_auction.auction.auction import Auction


class AuctionManager:
    def get_auction(self, db, id) -> Auction:
        db_obj = auction_crud.get(db, id)
        if db_obj:
            au_type = db_obj.type
            return factory.get_auction(au_type, db, db_obj=db_obj)

    def create_auction(self, db, obj_in, owner_id) -> Auction:
        return factory.get_new_auction(obj_in.type, db, obj_in, owner_id)

    def get_multi(self, db, *, skip, limit):
        return auction_crud.get_multi(db, skip=skip, limit=limit)


auction_manager = AuctionManager()
