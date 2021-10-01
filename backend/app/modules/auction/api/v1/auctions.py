from app.modules.user.models.user import User
from app.modules.auction.auction.english_auction import EnglishAuction
from datetime import datetime
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
    detail='only auction owner can do this action'
)

AUCTION_NOT_FOUND_EXCEPTION = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='auction not found'
)

router = APIRouter()


@router.put("/{id}/start")
def start_auction(*, id: int,
                  starting_date: datetime = Body(None),
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_active_user)):
    auction = auction_repo.get(db, id=id)
    if not auction:
        raise AUCTION_NOT_FOUND_EXCEPTION
    english = EnglishAuction()
    return english.start(db, db_obj=auction, starting_date=starting_date)


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
                   ending_date: datetime = Body(...),
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_active_user)):
    return auction_repo.create_with_owner(db, obj_in=auction_in, owner_id=current_user.id, ending_date=ending_date)


@router.get("/", response_model=List[AuctionInDB])
def get_auctions(*,
                 skip: int = 0,
                 limit: int = 5,
                 like: Optional[str] = None,
                 filter_by: Optional[str] = None,
                 db: Session = Depends(get_db)):
    return auction_repo.get_multi(db, skip=skip, limit=limit, like=like)
