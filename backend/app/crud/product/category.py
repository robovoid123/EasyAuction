from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.schemas.product import CategoryCreate, CategoryUpdate
from app.models.product import Category


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):

    def get_with_names(self, db: Session, names):
        return db.query(self.model).filter(self.model.name.in_(names)).all()


crud_category = CRUDCategory(Category)
