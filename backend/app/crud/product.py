from app.crud.base import CRUDBase
from app.schemas import product as cp
from app.models.product import Product


class CRUDProduct(CRUDBase[Product, cp.ProductCreate, cp.ProductUpdate]):
    pass


product = CRUDProduct(Product)
