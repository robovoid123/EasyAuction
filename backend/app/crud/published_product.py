from app.crud.base import CRUDBase
from app.schemas.market import (
    PublishedProductCreate,
    PublishedProductUpdate
)
from app.models.market import PublishedProduct


class CRUDPublishedProduct(CRUDBase[PublishedProduct, PublishedProductCreate,
                                    PublishedProductUpdate]):
    pass


published_product = CRUDPublishedProduct(PublishedProduct)
