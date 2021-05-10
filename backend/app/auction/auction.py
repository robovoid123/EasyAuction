from datetime import datetime
from fastapi import HTTPException

from app.schedule import schedule_task
from app.schemas.auction import AuctionSessionCreate, BidCreate
from app.models.auction import AuctionState, Bid

from app.crud.auction import auction
from app.crud.auction_session import auction_session
from app.crud.bid import bid


class Auction:
    def __init__(self, db, id):
        # TODO: need depenency for product
        self.db = db
        self.db_obj = None
        if id:
            self.db_obj = auction.get(db, id)

    @property
    def owner(self):
        return self.db_obj.owner

    def get(self):
        return self.db_obj

    def create(self, obj_in):
        return auction.create(self.db, obj_in=obj_in)

    def update(self, *, obj_in):
        return auction.update(self.db, db_obj=self.db_obj, obj_inj=obj_in)

    def remove(self):
        return auction.remove(self.db, id=self.db_obj.id)

    def create_auction_session(self, state, bid_line, auction_id):
        obj_in = AuctionSessionCreate(
            state=state,
            bid_line=bid_line,
            auction_id=auction_id
        )
        return auction_session.create(self.db, obj_in=obj_in)

    def create_bid(self, amount, bidder_id):
        obj_in = BidCreate(amount=amount, bidder_id=bidder_id)
        return bid.create(self.db, obj_in=obj_in)

    def schedule_ending(self, date, id):
        schedule_task(lambda: self.end(id), date)

    def _end_with_winner(self, auction):
        auction_session = auction.auction_session
        bid = auction_session.current_highest_bid

        auction.winner_id = bid.bidder_id
        auction.final_cost = auction_session.bid_line
        auction.is_ended = True
        # TODO: don't modify product here
        auction.product.inventory.quantity -= 1
        self.db.add(auction)
        self.db.commit()
        self.db.refresh(auction)
        return auction

    def reserve_met(self, auction):
        bid = auction.auction_session.current_highest_bid
        if auction.reserve and bid.amount < auction.reserve:
            return False
        return True

    def _cancel_auction(self, auction):
        auction_session = auction.auction_session

        auction.is_ended = True
        auction_session.state = AuctionState.CANCLED
        self.db.add(auction)
        self.db.add(auction_session)
        self.db.commit()

    def end(self):
        auction = self.db_obj
        auction_session = auction.auction_session

        if not auction_session:
            raise HTTPException(
                status_code=400,
                detail=""" auction has not yet started """
            )

        if auction_session.state == AuctionState.ONGOING:
            if auction_session.current_highest_bid:
                """
                somebody bid in the auction
                """
                if self.reserve_met(auction):
                    return self._end_with_winner(auction)
                else:
                    self._cancel_auction(auction)

                    raise HTTPException(
                        status_code=200,
                        detail=""" reserve not met so canceling auction """
                    )
            else:
                """
                no one bid in auction
                """
                if auction.ending_date < datetime.now():
                    """
                    timelimit is past end auction without winners
                    """
                    auction.is_ended = True
                    auction_session.state = AuctionState.ENDED
                    self.db.add(auction)
                    self.db.add(auction_session)
                    self.db.commit()
                    self.db.refresh(auction)
                    return auction
                else:
                    """
                    auction was canceled
                    """
                    self._cancel_auction(auction)
                    raise HTTPException(
                        status_code=200,
                        detail=""" canceling auction """
                    )

        elif auction_session.state in [AuctionState.ENDED, AuctionState.CANCLED]:
            raise HTTPException(
                status_code=400,
                detail=f" auction already ended {auction_session.state}"
            )

    def _start(self, auction):
        auction_session = auction.auction_session

        """
        if auction session is not created
        yet then we can start an auciton
        """
        if not auction_session:

            self.schedule_ending(auction.ending_date, id)

            self.create_auction_session(
                state=AuctionState.ONGOING,
                bid_line=auction.starting_bid_amount,
                auction_id=auction.id
            )
            auction.starting_date = datetime.now()

            self.db.add(auction)
            self.db.commit()
            self.db.refresh(auction)

            return auction

        else:

            """
            handle general errors here
            """
            raise HTTPException(
                status_code=400,
                detail=f" auction already {auction_session.state}"
            )

    def start(self, starting_date=None):
        auction = self.db_obj

        if starting_date:
            schedule_task(
                lambda: self._start(auction),
                starting_date
            )
            return f"auction has been scheduled for {starting_date}"

        else:
            self._start(auction)
            return "auction has been started"

    def bid(self, amount, user_id) -> Bid:
        pass
