from datetime import datetime
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException, status

from app.db.session import SessionLocal
from app.schedule import sched

from app.crud.base import CRUDBase
from app.schemas import auction as ap
from app.models.auction import Auction, AuctionSession, AuctionState, Bid
from app.auction.auction_method_factory import auction_method_factory


def schedule_task(func, date):
    # schedule auction ending

    job = sched.add_job(
        func,
        'date',
        run_date=date
    )

    print(job)


class CRUDAuction(CRUDBase[Auction, ap.AuctionCreate, ap.AuctionUpdate]):

    def task_create_auction_sess(self, obj_in):

        with SessionLocal() as db:

            self.create_auction_session(db, obj_in)

    def task_end_auction(self, id):

        with SessionLocal() as db:

            self.end_auction(db, id)

    def schedule_auction_ending(self, ending_date, id):

        schedule_task(
            lambda: self.task_end_auction(id),
            ending_date,
        )

    def schedule_auction_session_creation(self, starting_date, obj_in):

        print("Auction will start at: ", starting_date)

        obj_in = obj_in.dict()

        schedule_task(
            func=lambda: self.task_create_auction_sess(obj_in),
            date=starting_date
        )

    def create_auction_session(self, db, obj_in: ap.AuctionSessionCreate):

        obj_in_data = jsonable_encoder(obj_in)

        db_obj = AuctionSession(**obj_in_data)  # type: ignore

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def create_bid(self, db: Session, amount, bidder_id):

        db_obj = Bid(amount=amount, bidder_id=bidder_id)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def end_auction(self, db: Session, id):
        auction = self.get(db, id)

        if auction:

            auction_session = auction.auction_session

            if auction_session.state == AuctionState.ONGOING\
                    and auction_session.current_highest_bid_id:

                winning_bid = auction_session.current_highest_bid

                auction.winner_id = winning_bid.bidder_id
                auction.final_cost = auction_session.bid_line
                auction_session.state = AuctionState.ENDED
                auction.is_ended = True

            elif auction_session.state == AuctionState.ENDED:

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='auction already ended'
                )

            else:

                auction_session.state = AuctionState.CANCLED
                auction.is_ended = True

            db.add(auction)
            db.add(auction_session)
            db.commit()
            db.refresh(auction)

            return auction

        else:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='auction not found'
            )

    def start_auction(self, db: Session, id, starting_date=None):
        auction = self.get(db, id)

        if auction:

            auction_session = auction.auction_session

            if auction.is_ended or auction.ending_date < datetime.now():

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='auction has already ended'
                )

            if auction_session:

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='auction has already started'
                )

            obj_in = ap.AuctionSessionCreate(
                state=AuctionState.ONGOING,
                bid_line=auction.starting_bid_amount,
                auction_id=auction.id
            )

            self.schedule_auction_ending(auction.ending_date, id)

            if starting_date:
                self.schedule_auction_session_creation(starting_date, obj_in)
                auction.starting_date = starting_date
            else:
                self.create_auction_session(db, obj_in)
                auction.starting_date = datetime.now()

            db.add(auction)
            db.commit()
            db.refresh(auction)

            return auction

        else:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='auction not found'
            )

    def bid(self, db: Session, id, amount, user_id) -> Bid:

        auction = self.get(db, id)

        if auction:

            auction_session = auction.auction_session

            if not auction_session:

                pass

            invalid_states = [AuctionState.ENDED, AuctionState.CANCLED]

            if auction.is_ended or \
                auction_session.state in invalid_states \
                    or auction.ending_date < datetime.now():

                pass

            elif auction_session.state == AuctionState.ONGOING:

                bid = self.create_bid(db, amount, user_id)

                auction_session.last_bid_at = bid.created_at
                auction_session.bids.append(bid)

                method = auction_method_factory.get_method(auction.type)

                auction, auction_session = method(db, auction, auction_session, bid)

                db.add(auction)
                db.add(auction_session)
                db.commit()

                return bid

            else:

                """ this will probably never happen """

        else:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='auction not found'
            )


auction = CRUDAuction(Auction)
