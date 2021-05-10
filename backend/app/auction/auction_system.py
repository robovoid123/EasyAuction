from app.crud.auction import auction as auction_crud

from app.auction.auction_factory import factory
from app.auction.auction import Auction


class AuctionSystem:
    def get_auction(self, db, id) -> Auction:
        auction = auction_crud.get(db, id)

        if not auction:
            """
            auction not found
            """

        au_type = auction.type
        return factory.get_auction(au_type, db, id=id)

    def create_auction(self, db, obj_in):
        auction_creator = factory.get_auction(obj_in.type, db)
        return auction_creator.create(obj_in)

    def get_multi(self, db, *, skip, limit):
        return auction_crud.get_multi(db, skip=skip, limit=limit)


auction_system = AuctionSystem()
