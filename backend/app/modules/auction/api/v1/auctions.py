from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.dependencies.auth import get_current_active_user

from app.modules.auction.models import AuctionState
from app.modules.auction.schemas import (AuctionCreate, AuctionCreateRequest, AuctionResponse, AuctionSessionInDB,
                                         AuctionUpdate,
                                         AuctionInDB,
                                         BidInDB)
from app.easy_auction.auction_factory import auction_factory
from app.modules.auction.repositories import auction_repo

OWNER_ONLY_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='only auction owner can do this action'
)

AUCTION_NOT_FOUND_EXCEPTION = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='auction not found'
)

router = APIRouter()


@router.post('/', response_model=AuctionInDB)
def create_auction(*,
                   db: Session = Depends(get_db),
                   current_user=Depends(get_current_active_user),
                   auction_in: AuctionCreateRequest):

    obj_in = AuctionCreate(**auction_in.dict(exclude_unset=True))
    auction = auction_factory.get_auction(auction_in.au_type)
    db_obj = auction.create(db, obj_in=obj_in, owner_id=current_user.id,
                            ending_date=auction_in.ending_date)
    obj = jsonable_encoder(db_obj)
    if db_obj.session:
        state = db_obj.session.state
        bid_line = db_obj.session.bid_line
        last_bid_at = db_obj.session.last_bid_at
        obj["state"] = state
        obj["bid_line"] = bid_line
        obj["last_bid_at"] = last_bid_at

    return obj


@router.get('/', response_model=List[AuctionInDB])
def get_auctions(*,
                 db: Session = Depends(get_db),
                 skip: int = 0,
                 limit: int = 5):

    return auction_repo.get_multi(db, skip=skip, limit=limit)


@router.post('/{id}/start', response_model=AuctionSessionInDB)
def start_auction(id,
                  *,
                  db: Session = Depends(get_db),
                  starting_date: datetime = Query(None),
                  current_user=Depends(get_current_active_user)
                  ):

    db_obj = auction_repo.get(db, id)

    if not db_obj:
        raise AUCTION_NOT_FOUND_EXCEPTION

    if db_obj.owner_id != current_user.id:
        raise OWNER_ONLY_EXCEPTION
    auction = auction_factory.get_auction(db_obj.au_type)

    return auction.start(db, id=id, starting_date=starting_date)


# @router.post('/{id}/end', response_model=AuctionInDB)
# def end_auction(id,
#                 *,
#                 db: Session = Depends(get_db),
#                 current_user=Depends(get_current_active_user)):

#     auction = Auction(db)
#     db_obj = auction.get(id)

#     if not db_obj:
#         raise AUCTION_NOT_FOUND_EXCEPTION

#     if db_obj.owner_id != current_user.id:
#         raise OWNER_ONLY_EXCEPTION

#     return auction.end(id)

@router.post('/{id}/cancel', response_model=AuctionSessionInDB)
def cancel_auction(id,
                   *,
                   db: Session = Depends(get_db),
                   current_user=Depends(get_current_active_user)):

    db_obj = auction_repo.get(db, id)

    if not db_obj:
        raise AUCTION_NOT_FOUND_EXCEPTION

    if db_obj.owner_id != current_user.id:
        raise OWNER_ONLY_EXCEPTION
    auction = auction_factory.get_auction(db_obj.au_type)

    return auction.cancel(db, id)


@router.post('/{id}/bids', response_model=BidInDB)
def bid(id,
        *,
        db: Session = Depends(get_db),
        amount: int = Body(...),
        current_user=Depends(get_current_active_user)):

    db_obj = auction_repo.get(db, id)

    if not db_obj:

        raise AUCTION_NOT_FOUND_EXCEPTION
    auction = auction_factory.get_auction(db_obj.au_type)
    return auction.bid(db, id, amount, current_user.id)


@router.post('/{id}/buy_it_now', response_model=AuctionSessionInDB)
def buy_it_now(id,
               *,
               db: Session = Depends(get_db),
               current_user=Depends(get_current_active_user)):

    db_obj = auction_repo.get(db, id)

    if not db_obj:
        raise AUCTION_NOT_FOUND_EXCEPTION
    auction = auction_factory.get_auction(db_obj.au_type)

    return auction.buy_it_now(db, id, current_user.id)


@router.get('/{id}', response_model=AuctionResponse)
def get_auction(id,
                *,
                db: Session = Depends(get_db)):

    db_obj = auction_repo.get(db, id)

    if not db_obj:
        raise AUCTION_NOT_FOUND_EXCEPTION

    obj = jsonable_encoder(db_obj)
    if db_obj.session:
        state = db_obj.session.state
        bid_line = db_obj.session.bid_line
        last_bid_at = db_obj.session.last_bid_at
        obj["state"] = state
        obj["bid_line"] = bid_line
        obj["last_bid_at"] = last_bid_at
    return obj


@router.put('/{id}', response_model=AuctionInDB)
def update_auction(id,
                   *,
                   db: Session = Depends(get_db),
                   current_user=Depends(get_current_active_user),
                   auction_in: AuctionUpdate):

    db_obj = auction_repo.get(db, id)

    if not db_obj:
        raise AUCTION_NOT_FOUND_EXCEPTION

    if db_obj.owner_id != current_user.id:
        raise OWNER_ONLY_EXCEPTION

    if db_obj.auction_session and\
            not db_obj.auction_session.status == AuctionState.ONGOING:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="""can\'t update an already started auction.
             either end or pause the auction"""
        )
    auction = auction_factory.get_auction(db_obj.au_type)

    db_obj = auction.update(db, db_obj, auction_in)
    obj = jsonable_encoder(db_obj)
    if db_obj.session:
        state = db_obj.session.state
        bid_line = db_obj.session.bid_line
        last_bid_at = db_obj.session.last_bid_at
        obj["state"] = state
        obj["bid_line"] = bid_line
        obj["last_bid_at"] = last_bid_at
    return obj
