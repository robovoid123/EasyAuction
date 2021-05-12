from app.crud.base import CRUDBase
from app.schemas.market import (
    BuyHistoryCreate,
    BuyHistoryUpdate
)
from app.models.market import BuyHistory


class CRUDBuyHistory(CRUDBase[BuyHistory, BuyHistoryCreate,
                              BuyHistoryUpdate]):
    pass


buy_history = CRUDBuyHistory(BuyHistory)
