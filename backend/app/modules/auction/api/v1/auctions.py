from app.modules.user.models.user import User
from app.modules.auction.auction.english_auction import EnglishAuction
from datetime import datetime
from app.modules.auction.models.auction_state import AuctionState
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from typing import List, Optional

from app.dependencies.database import get_db
from app.dependencies.auth import get_current_active_user

from app.modules.auction.schemas import (AuctionCreate,
                                         AuctionUpdate,
                                         AuctionInDB,)

from app.modules.auction.repositories import auction_repo

OWNER_ONLY_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='You do not have enough privilege to do this action'
)

AUCTION_NOT_FOUND_EXCEPTION = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Auction not found'
)

AUCTION_NOT_STARTED_EXCEPTION = HTTPException(
    status_code=400,
    detail='Auction has not yet been started'
)

router = APIRouter()


@router.put("/{id}/start")
def start_auction(*, id: int,
                  starting_date: datetime = Body(None),
                  ending_date: datetime = Body(...),
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_active_user)):
    auction = auction_repo.get(db, id=id)
    if not auction:
        raise AUCTION_NOT_FOUND_EXCEPTION
    english = EnglishAuction()
    return english.start(db, db_obj=auction, starting_date=starting_date, ending_date=ending_date)


@router.put("/{id}/end")
def end_auction(*, id: int,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_active_user)):
    auction = auction_repo.get(db, id=id)
    if not auction:
        raise AUCTION_NOT_FOUND_EXCEPTION
    english = EnglishAuction()
    return english.end(db, db_obj=auction)


@router.post("/{id}/bid")
def bid_in_auction(*, id: int,
                   amount: float = Body(...),
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_active_user)):
    auction = auction_repo.get(db, id=id)
    if not auction:
        raise AUCTION_NOT_FOUND_EXCEPTION

    if auction.state != AuctionState.ONGOING:
        raise AUCTION_NOT_STARTED_EXCEPTION

    english = EnglishAuction()
    return english.bid(db, db_obj=auction, amount=amount, bidder_id=current_user.id)


@router.post("/{id}/buy_it_now")
def buy_it_now(*, id: int,
               db: Session = Depends(get_db),
               current_user: User = Depends(get_current_active_user)):
    auction = auction_repo.get(db, id=id)
    if not auction:
        raise AUCTION_NOT_FOUND_EXCEPTION
    english = EnglishAuction()
    return english.buy_it_now(db, db_obj=auction, buyer_id=current_user.id)


@router.put("/{id}")
def update_auction(*, id: int,
                   auction_in: AuctionUpdate,
                   ending_date: datetime = Body(None),
                   db: Session = Depends(get_db)):
    auction = auction_repo.get(db, id=id)
    if not auction:
        raise AUCTION_NOT_FOUND_EXCEPTION
    return auction_repo.update_with_date(db, db_obj=auction, obj_in=auction_in, ending_date=ending_date)


@router.get("/{id}", response_model=AuctionInDB)
def get_auction(*, id: int,
                db: Session = Depends(get_db)):
    auction = auction_repo.get(db, id=id)
    if not auction:
        raise AUCTION_NOT_FOUND_EXCEPTION
    return auction


@router.delete("/{id}")
def delete_auction(*, id: int,
                   db: Session = Depends(get_db)):
    auction = auction_repo.get(db, id=id)
    if not auction:
        raise AUCTION_NOT_FOUND_EXCEPTION
    return auction_repo.remove(db, id=id)


@router.post("/", status_code=201)
def create_auction(*,
                   auction_in: AuctionCreate,
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_active_user)):
    return auction_repo.create_with_owner(db, obj_in=auction_in, owner_id=current_user.id)


@router.get("/", response_model=List[AuctionInDB])
def get_auctions(*,
                 skip: int = 0,
                 limit: int = 5,
                 states: Optional[str] = 'ongoing,ended',
                 like: Optional[str] = None,
                 order_by: Optional[str] = 'last_bid_at',
                 is_desc: Optional[bool] = True,
                 db: Session = Depends(get_db)):
    """
                ## order by available options\n
                - bid_count 
                - starting_bid_amount
                - bid_cap
                - starting_date
                - ending_date
                - last_bid_at
                - reserve

                -----------\n

                ## states available options\n
                - ongoing
                - started
                - ended
                - canceled

    """
    states = states.split(',')
    return auction_repo.get_multi(db, skip=skip, limit=limit, like=like, states=states, order_by=order_by, is_desc=is_desc)


@router.get("/users/{user_id}", response_model=List[AuctionInDB])
def get_users_auction(*,
                      user_id: int,
                      skip: int = 0,
                      limit: int = 5,
                      states: Optional[str] = 'ongoing,ended',
                      order_by: Optional[str] = 'last_bid_at',
                      is_desc: Optional[bool] = True,
                      db: Session = Depends(get_db)):
    """
                ## order by available options\n
                - bid_count 
                - starting_bid_amount
                - bid_cap
                - starting_date
                - ending_date
                - last_bid_at
                - reserve

                -----------\n

                ## states available options\n
                - ongoing
                - started
                - ended
                - canceled

    """
    states = states.split(',')
    return auction_repo.get_multi_by_user(db, skip=skip, limit=limit, states=states, order_by=order_by, is_desc=is_desc, user_id=user_id)
