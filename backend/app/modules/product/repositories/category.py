from typing import Optional, List
from sqlalchemy.orm import Session

from app.repository.repository_base import BaseRepository

from app.modules.product.schemas import CategoryCreate, CategoryUpdate
from app.modules.product.models import Category


class CategoryRepository(BaseRepository[Category, CategoryCreate, CategoryUpdate]):

    def get_with_name(self, db: Session, name: str) -> Optional[Category]:
        return db.query(self.model).filter(self.model.name == name).first()

    def get_with_names(self, db: Session, names) -> Optional[List[Category]]:
        return db.query(self.model).filter(self.model.name.in_(names)).all()

    def get_multi_with_ids(self, db: Session, ids: List[int]) -> List[Category]:
        return db.query(self.model).filter(self.model.id.in_(ids)).all()


category_repo = CategoryRepository(Category)
