from fastapi import APIRouter
from .v1 import auctions, bids

router = APIRouter()

router.include_router(auctions.router, prefix="/auctions", tags=["Auction"])
router.include_router(bids.router, prefix="/bids", tags=["Bid"])
