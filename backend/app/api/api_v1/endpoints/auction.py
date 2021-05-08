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
from app.crud.auction import auction as ac

router = APIRouter()


@router.post('/', response_model=AuctionInDB)
def create_auction(
    *,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
    auction_in: AuctionCreate
):

    auction = ac.create(db=db, obj_in=auction_in)

    return auction


@router.get('/', response_model=List[AuctionInDB])
def get_auctions(*,
                 db: Session = Depends(get_db),
                 skip: int = 0,
                 limit: int = 5):

    return ac.get_multi(db=db, skip=skip, limit=limit)


@router.post('/{id}/start', response_model=AuctionInDB)
def start_auction(id,
                  *,
                  db: Session = Depends(get_db),
                  starting_date: datetime = Query(None),
                  current_user=Depends(get_current_active_user)
                  ):

    auction = ac.get(db=db, id=id)

    if not auction:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='auction not found'
        )

    if auction.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='only auction owner can do this action'
        )

    return ac.start_auction(db, id, starting_date)


@router.post('/{id}/end', response_model=AuctionInDB)
def end_auction(id,
                *,
                db: Session = Depends(get_db),
                current_user=Depends(get_current_active_user)):

    auction = ac.get(db=db, id=id)

    if not auction:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='auction not found'
        )

    if auction.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='only auction owner can do this action'
        )

    return ac.end_auction(db)


@router.post('/{id}/bids', response_model=BidInDB)
def bid_in_auction(id,
                   *,
                   db: Session = Depends(get_db),
                   amount: int = Body(...),
                   current_user=Depends(get_current_active_user)):

    auction = ac.get(db=db, id=id)

    if not auction:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='auction not found'
        )

    return ac.bid(db, id, amount, current_user.id)


@router.get('/{id}', response_model=AuctionInDB)
def get_auction(id,
                *,
                db: Session = Depends(get_db)):

    auction = ac.get(db=db, id=id)

    if not auction:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='auction not found'
        )

    return auction


@router.put('/{id}', response_model=AuctionInDB)
def update_auction(id,
                   *,
                   db: Session = Depends(get_db),
                   current_user=Depends(get_current_active_user),
                   auction_in: AuctionUpdate,
                   end_auction: bool = False):

    auction = ac.get(db=db, id=id)

    if not auction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='auction not found'
        )

    if auction.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='only auction owner can do this action'
        )

    if end_auction:
        ac.end_auction(db)

    if auction.auction_session and\
            not auction.auction_session.status == AuctionState.ONGOING:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="""can\'t update an already started auction.
             either end or pause the auction"""
        )

    return ac.update(db, db_obj=auction, obj_in=auction_in)
