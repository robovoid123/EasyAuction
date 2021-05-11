from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.api.dependencies.auth import get_current_active_user

from app.models.auction import AuctionState
from app.schemas.auction import (AuctionCreate,
                                 AuctionUpdate,
                                 AuctionInDB,
                                 BidInDB)

from app.easy_auction.auction.auction_manager import auction_manager

router = APIRouter()


@router.post('/', response_model=AuctionInDB)
def create_auction(
    *,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
    auction_in: AuctionCreate
):

    return auction_manager.create_auction(db, auction_in, owner_id=current_user.id).get()


@router.get('/', response_model=List[AuctionInDB])
def get_auctions(*,
                 db: Session = Depends(get_db),
                 skip: int = 0,
                 limit: int = 5):

    return auction_manager.get_multi(db, skip=skip, limit=limit)


@router.post('/{id}/start')
def start_auction(id,
                  *,
                  db: Session = Depends(get_db),
                  starting_date: datetime = Query(None),
                  current_user=Depends(get_current_active_user)
                  ):

    auction = auction_manager.get_auction(db, id)

    if not auction:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='auction not found'
        )

    if auction.owner.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='only auction owner can do this action'
        )

    return auction.start(starting_date=starting_date)


@router.post('/{id}/end', response_model=AuctionInDB)
def end_auction(id,
                *,
                db: Session = Depends(get_db),
                current_user=Depends(get_current_active_user)):

    auction = auction_manager.get_auction(db, id)

    if not auction:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='auction not found'
        )

    if auction.owner.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='only auction owner can do this action'
        )

    return auction.end()


@router.post('/{id}/bids', response_model=BidInDB)
def bid_in_auction(id,
                   *,
                   db: Session = Depends(get_db),
                   amount: int = Body(...),
                   current_user=Depends(get_current_active_user)):

    auction = auction_manager.get_auction(db, id)

    if not auction:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='auction not found'
        )
    return auction.bid(amount, current_user.id)


@router.get('/{id}', response_model=AuctionInDB)
def get_auction(id,
                *,
                db: Session = Depends(get_db)):

    auction = auction_manager.get_auction(db, id)

    if not auction:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='auction not found'
        )

    return auction.get()


@router.put('/{id}', response_model=AuctionInDB)
def update_auction(id,
                   *,
                   db: Session = Depends(get_db),
                   current_user=Depends(get_current_active_user),
                   auction_in: AuctionUpdate,
                   end_auction: bool = False):

    auction = auction_manager.get_auction(db, id)

    if not auction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='auction not found'
        )

    if auction.owner.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='only auction owner can do this action'
        )

    if end_auction:
        auction.end()

    if auction.auction_session and\
            not auction.auction_session.status == AuctionState.ONGOING:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="""can\'t update an already started auction.
             either end or pause the auction"""
        )

    return auction.update(auction_in)
