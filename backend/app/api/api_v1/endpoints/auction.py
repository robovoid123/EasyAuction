from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_user

from app.api.dependencies.database import get_db
from app.api.dependencies.auth import get_current_active_user

from app.models.auction import AuctionState
from app.schemas.auction import (AuctionCreate, AuctionCreateRequest,
                                 AuctionUpdate,
                                 AuctionInDB,
                                 BidInDB)
from app.crud.auction.auction import crud_auction
from app.easy_auction.auction_factory import auction_factory

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

    auction_in = AuctionCreate(**auction_in.dict(), owner_id=current_user.id)
    auction = auction_factory.get_auction(auction_in.au_type)
    return auction.create(db, auction_in)


@router.get('/', response_model=List[AuctionInDB])
def get_auctions(*,
                 db: Session = Depends(get_db),
                 skip: int = 0,
                 limit: int = 5):

    return crud_auction.get_multi(db, skip=skip, limit=limit)


@router.post('/{id}/start')
def start_auction(id,
                  *,
                  db: Session = Depends(get_db),
                  starting_date: datetime = Query(None),
                  current_user=Depends(get_current_active_user)
                  ):

    db_obj = crud_auction.get(db, id)
    auction = auction_factory.get_auction(db_obj.au_type)

    if not db_obj:
        raise AUCTION_NOT_FOUND_EXCEPTION

    if db_obj.owner_id != current_user.id:
        raise OWNER_ONLY_EXCEPTION

    return auction.start(db, id, starting_date=starting_date)


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

@router.post('/{id}/cancel', response_model=AuctionInDB)
def cancel_auction(id,
                   *,
                   db: Session = Depends(get_db),
                   current_user=Depends(get_current_active_user)):

    db_obj = crud_auction.get(db, id)
    auction = auction_factory.get_auction(db_obj.au_type)

    if not db_obj:
        raise AUCTION_NOT_FOUND_EXCEPTION

    if db_obj.owner_id != current_user.id:
        raise OWNER_ONLY_EXCEPTION

    return auction.cancel(db, id)


@router.post('/{id}/bids', response_model=BidInDB)
def bid(id,
        *,
        db: Session = Depends(get_db),
        amount: int = Body(...),
        current_user=Depends(get_current_active_user)):

    db_obj = crud_auction.get(db, id)
    auction = auction_factory.get_auction(db_obj.au_type)

    if not db_obj:

        raise AUCTION_NOT_FOUND_EXCEPTION
    return auction.bid(db, id, amount, current_user.id)


@router.post('/{id}/buy_it_now', response_model=AuctionInDB)
def buy_it_now(id,
               *,
               db: Session = Depends(get_db),
               current_user=Depends(get_current_active_user)):

    db_obj = crud_auction.get(db, id)
    auction = auction_factory.get_auction(db_obj.au_type)

    if not db_obj:
        raise AUCTION_NOT_FOUND_EXCEPTION

    return auction.buy_it_now(db, id, current_user.id)


@router.get('/{id}', response_model=AuctionInDB)
def get_auction(id,
                *,
                db: Session = Depends(get_db)):

    db_obj = crud_auction.get(db, id)

    if not db_obj:
        raise AUCTION_NOT_FOUND_EXCEPTION

    return db_obj


@router.put('/{id}', response_model=AuctionInDB)
def update_auction(id,
                   *,
                   db: Session = Depends(get_db),
                   current_user=Depends(get_current_active_user),
                   auction_in: AuctionUpdate):

    db_obj = crud_auction.get(db, id)
    auction = auction_factory.get_auction(db_obj.au_type)

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

    return auction.update(db, db_obj, auction_in)
