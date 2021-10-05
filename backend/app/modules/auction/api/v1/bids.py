
from typing import Dict, List, Tuple
from app.modules.auction.schemas.auction import AuctionInDB
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.database import get_db

from app.modules.auction.repositories.bid import bid_repo

router = APIRouter()


@router.get("/{bidder_id}/auctions", response_model=List[AuctionInDB])
def get_bidder_bid_auctions(*,
                            bidder_id: int,
                            skip: int = 0,
                            limit: int = 5,
                            db: Session = Depends(get_db)
                            ):
    api_resp = bid_repo.get_bidder_auction(
        db, skip=skip, limit=limit, bidder_id=bidder_id)
    return api_resp
