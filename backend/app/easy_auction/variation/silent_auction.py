from datetime import datetime
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session, session


from app.models.auction import AuctionState, Bid, AuctionSession, Auction as AuctionModel
from app.easy_auction.auction import Auction

from app.schedule import sched
from app.crud.auction.auction import crud_auction
from app.crud.auction.auction_session import crud_auctionsession
from app.crud.product.product import crud_product
from app.crud.auction.bid import crud_bid

from app.schemas.auction import AuctionSessionCreate, AuctionSessionUpdate, AuctionUpdate, BidCreate


class SilentAuction(Auction):
    def _start(): pass
    def _end(): pass
    def _bid(): pass
