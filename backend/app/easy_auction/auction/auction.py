from typing import Optional
from datetime import datetime
from fastapi import HTTPException

from app.schedule import schedule_task
from app.schemas.auction import AuctionSessionCreate, BidCreate
from app.models.auction import AuctionState, Bid, Auction as AuctionModel

from app.crud.auction import auction as crud
from app.crud.auction_session import auction_session as session_crud
from app.crud.bid import bid as bid_crud

from app.easy_auction.product.product_manager import product_manager

"""
mapped SQLAlchemy model and added functionality over it
"""


class Auction:
    def __init__(self, db, id=None, db_obj=None):
        self.db = db
        self.db_obj = None
        if id:
            self.db_obj = crud.get(db, id)
        elif db_obj:
            self.db_obj = db_obj

        if self.db_obj:
            product_db_obj = self.db_obj.product
            self._product = product_manager.populate_from_obj(db, product_db_obj)

    @property
    def owner(self): return self.db_obj.owner

    @property
    def auction_session(self): return self.db_obj.auction_session

    @property
    def product(self): return self._product

    @property
    def starting_bid_amount(self): return self.db_obj.starting_bid_amount

    @property
    def bid_cap(self): return self.db_obj.bid_cap

    @property
    def reserve(self): return self.db_obj.reserve

    @property
    def ending_date(self): return self.db_obj.ending_date

    @property
    def starting_date(self): return self.db_obj.starting_date

    @property
    def type(self): return self.db_obj.type

    @property
    def final_cost(self): return self.db_obj.final_cost

    @property
    def is_ended(self): return self.db_obj.is_ended

    @property
    def winner(self): return self.db_obj.winner

    @classmethod
    def create(cls, db, obj_in, owner_id):
        db_obj = crud.create_with_owner(db, obj_in=obj_in, owner_id=owner_id)
        return cls(db, db_obj=db_obj)

    def get(self) -> Optional[AuctionModel]:
        return self.db_obj

    def update(self, obj_in) -> AuctionModel:
        return crud.update(self.db, db_obj=self.db_obj, obj_in=obj_in)

    def remove(self):
        return crud.remove(self.db, id=self.db_obj.id)

    def update_session(self, obj_in):
        return session_crud.update(self.db,
                                   db_obj=self.db_obj.auction_session,
                                   obj_in=obj_in)

    def create_auction_session(self, state, bid_line, auction_id):
        obj_in = AuctionSessionCreate(
            state=state,
            bid_line=bid_line,
            auction_id=auction_id
        )
        return session_crud.create(self.db, obj_in=obj_in)

    def add_session(self, state, bid_line, auction_id):
        new_session = self.create_auction_session(
            state=state,
            bid_line=bid_line,
            auction_id=auction_id
        )
        self.db_obj.auction_session = new_session
        self.db.add(self.db_obj)
        self.db.commit()
        self.db.refresh(self.db_obj)

    def create_bid(self, amount, bidder_id):
        obj_in = BidCreate(amount=amount, bidder_id=bidder_id)
        return bid_crud.create(self.db, obj_in=obj_in)

    def append_bid(self, bid):
        self.db_obj.auction_session.bids.append(bid)
        self.db.add(self.db_obj)
        self.db.commit()
        self.db.refresh(self.db_obj)

    def schedule_ending(self, date, id):
        schedule_task(lambda: self.end(id), date)

    def _end_with_winner(self):
        bid = self.auction_session.current_highest_bid

        self.update({
            'winner_id': bid.bidder_id,
            'final_cost': self.auction_session.bid_line,
            'is_ended': True
        })
        self.update_session({'state': AuctionState.ENDED})
        return self.db_obj

    def reserve_met(self):
        bid = self.auction_session.current_highest_bid
        if self.db_obj.reserve and bid.amount < self.db_obj.reserve:
            return False
        return True

    def _cancel_auction(self):
        self.update({'is_ended': True})
        self.update_session({'state': AuctionState.CANCLED})
        self.product.free(1)

    def end(self):
        if not self.auction_session:
            raise HTTPException(
                status_code=400,
                detail="auction has not yet started"
            )

        if self.auction_session.state == AuctionState.ONGOING:
            if self.auction_session.current_highest_bid:
                """
                somebody bid in the auction
                """
                if self.reserve_met():
                    self._end_with_winner()
                    return "ending auction with a winner"
                else:
                    self._cancel_auction()
                    return "reserve not met so canceling auction"
            else:
                """
                no one bid in auction
                """
                if self.db_obj.ending_date < datetime.now():
                    """
                    timelimit is past end auction without winners
                    """
                    self.update({'is_ended': True})
                    self.update_session({'state': AuctionState.ENDED})
                    self.product.free(1)
                    return "ending auction without winner"
                else:
                    """
                    auction was canceled
                    """
                    self._cancel_auction()
                    return "canceling auction"

        elif self.auction_session.state in [AuctionState.ENDED, AuctionState.CANCLED]:
            raise HTTPException(
                status_code=400,
                detail=f"auction already ended {self.auction_session.state}"
            )

    def _start(self):
        """
        if auction session is not created
        yet then we can start an auciton
        """
        if not self.auction_session:

            self.schedule_ending(self.db_obj.ending_date, id)

            # TODO: remove auction_id
            self.add_session(
                state=AuctionState.ONGOING,
                bid_line=self.db_obj.starting_bid_amount,
                auction_id=self.db_obj.id
            )

            self.update({'starting_date': datetime.now()})

            # reserving product for auction
            # TODO: look for better implementation like reserve and free method
            # TODO: make able to auction multiple item at once
            self.product.reserve(1)

        else:

            """
            handle general errors here
            """
            raise HTTPException(
                status_code=400,
                detail=f"auction already {self.auction_session.state}"
            )

    def start(self, starting_date=None):
        if starting_date:
            schedule_task(
                lambda: self._start(),
                starting_date
            )
            return f"auction has been scheduled for {starting_date}"

        else:
            self._start()
            return "auction has been started"

    def buy_it_now(self):
        # TODO: implement
        pass

    def bid(self, amount, user_id) -> Bid:
        pass
