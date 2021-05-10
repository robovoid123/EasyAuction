from app.crud.base import CRUDBase
from app.schemas import auction as ap
from app.models.auction import Auction


class CRUDAuction(CRUDBase[Auction, ap.AuctionCreate, ap.AuctionUpdate]):
    pass


auction = CRUDAuction(Auction)
