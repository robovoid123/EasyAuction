from typing import List
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.schemas import product as ps
from app.models.product import Category


class CRUDCategory(CRUDBase[Category, ps.CategoryCreate, ps.CategoryUpdate]):
    def get_with_name(self, db: Session, name: str) -> Category:
        return db.query(self.model).filter(self.model.name == name).first()

    def get_with_names(self, db: Session, names: List[str]) -> List[Category]:
        return db.query(self.model).filter(self.model.name.in_(names)).all()


category = CRUDCategory(Category)
