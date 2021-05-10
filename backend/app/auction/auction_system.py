from app.crud.auction import auction
from app.crud.bid import bid
from app.crud.auction_session import auction_session

from app.auction.auction_factory import factory
from app.auction.auction import Auction


class AuctionSystem:
    def __init__(self, bid_crud, auction_crud, auction_session_crud):
        self.bid_crud = bid_crud
        self.auction_crud = auction_crud
        self.auction_session_crud = auction_session_crud

    def get_auction(self, db, id) -> Auction:
        auction = self.auction_crud.get(db, id)

        if not auction:
            """
            auction not found
            """
            return

        au_type = auction.type
        return factory.get_auction(au_type, db,
                                   crud_auction=self.auction_crud,
                                   crud_auction_session=self.auction_session_crud,
                                   crud_bid=self.bid_crud,
                                   id=id)

    def create_auction(self, db, obj_in):
        auction_creator = factory.get_auction(
            obj_in.type, db,
            crud_auction=self.auction_crud,
            crud_auction_session=self.auction_session_crud,
            crud_bid=self.bid_crud)
        return auction_creator.create(obj_in)

    def get_multi(self, db, *, skip, limit):
        return self.auction_crud.get_multi(db, skip=skip, limit=limit)


auction_system = AuctionSystem(bid, auction, auction_session)
