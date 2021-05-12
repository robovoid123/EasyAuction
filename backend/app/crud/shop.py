from app.crud.base import CRUDBase
from app.schemas.market import (
    ShopCreate,
    ShopUpdate
)
from app.models.market import Shop


class CRUDShop(CRUDBase[Shop, ShopCreate, ShopUpdate]):
    pass


shop = CRUDShop(Shop)
