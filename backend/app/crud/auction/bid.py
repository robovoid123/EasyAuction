from app.crud.base import CRUDBase
from app.schemas import auction as ap
from app.models.auction import Bid


class CRUDBid(CRUDBase[Bid, ap.BidCreate,
                       ap.BidUpdate]):
    pass


crud_bid = CRUDBid(Bid)
