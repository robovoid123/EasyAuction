from datetime import datetime
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session, session


from app.models.auction import AuctionState, Bid, AuctionSession, Auction as AuctionModel
from app.easy_auction.auction import Auction

from app.crud.auction.auction import crud_auction
from app.crud.auction.auction_session import crud_auctionsession
from app.crud.product.product import crud_product

from app.schemas.auction import AuctionSessionCreate, AuctionSessionUpdate, AuctionUpdate


class EnglishAuction(Auction):

    INC_AMT = 1.25

    def _start(self, db: Session, id: int) -> AuctionSession:
        db_obj = crud_auction.get(id)
        sess_obj = AuctionSessionCreate(
            state=AuctionState.ONGOING,
            bid_line=db_obj.starting_bid_amount,
            bid_cap=db_obj.bid_cap,
            reserve=db_obj.reserve,
            auction_id=db_obj.id
        )
        session_db = crud_auctionsession.create(db, sess_obj)
        auc_obj = AuctionUpdate(starting_date=datetime.now())
        crud_auction.update(db, db_obj, auc_obj)
        return session_db

    def _reserve_met(self, session: AuctionSession) -> bool:
        bid: Bid = session.winning_bid
        if session.reserve and bid.amount < session.reserve:
            return False
        return True

    def _end_with_winner(self, db_obj: AuctionModel, bid: Bid):
        auc_obj = AuctionUpdate(
            winner_id=bid.bidder_id,
            final_cost=db_obj.session.bid_line,
            is_ended=True,
            ending_date=datetime.now()
        )
        crud_auction.update(db_obj, auc_obj)
        sess_obj = AuctionSessionUpdate(state=AuctionState.ENDED)
        crud_auctionsession.update(db_obj.auction_session, sess_obj)

    def _end_without_winner(self, db_obj: AuctionModel) -> None:
        auc_obj = AuctionUpdate(is_ended=True, ending_date=datetime.now())
        crud_auction.update(db_obj, auc_obj)
        sess_obj = AuctionSessionUpdate(state=AuctionState.ENDED)
        crud_auctionsession.update(db_obj.auction_session, sess_obj)
        crud_product.free(db_obj.product_id, 1)

    def _end(self, db: Session, id: int) -> None:
        db_obj = crud_auction.get(id)
        session: AuctionSession = db_obj.session

        if session.winning_bid:
            winning_bid: Bid = session.winning_bid
            if self._reserve_met(session):
                self._end_with_winner(db_obj, winning_bid)
            else:
                self._end_without_winner(db_obj)
        else:
            self._end_without_winner(db_obj)

    def _bid(self, db: Session, id: int, new_bid: Bid) -> Bid:
        db_obj = crud_auction.get(id)
        session: AuctionSession = db_obj.session

        if new_bid.amount > session.bid_line:
            new_bid_line = new_bid.amount + EnglishAuction.INC_AMT
            if new_bid_line >= session.bid_cap:
                new_bid_line = session.bid_cap

            sess_obj = AuctionSessionUpdate(
                winning_bid_id=new_bid.id,
                last_bid_at=datetime.now(),
                bid_line=new_bid_line
            )
            crud_auctionsession.update(session, sess_obj)
            return new_bid
        else:
            abl = session.bid_line
            raise HTTPException(status_code=400,
                                detail=f"bid amount must be greater than {abl}")
