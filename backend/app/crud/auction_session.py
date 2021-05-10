from app.crud.base import CRUDBase
from app.schemas import auction as ap
from app.models.auction import AuctionSession


class CRUDAuctionSession(CRUDBase[AuctionSession, ap.AuctionSessionCreate,
                                  ap.AuctionSessionUpdate]):
    pass


auction_session = CRUDAuctionSession(AuctionSession)
