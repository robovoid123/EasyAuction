from app.crud.base import CRUDBase
from app.schemas import product as ps
from app.models.product import Category


class CRUDCategory(CRUDBase[Category, ps.CategoryCreate, ps.CategoryUpgrade]):
    def get_with_name(self, db, name):
        pass


category = CRUDCategory(Category)
