from typing import List

from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.repository.repository_base import BaseRepository

from app.modules.product.schemas import ProductCreate, ProductUpdate
from app.modules.product.models import Product, Category


class ProductRepository(BaseRepository[Product, ProductCreate, ProductUpdate]):
    def create_with_user(self, db: Session, *,
                         obj_in: ProductCreate, owner_id: int) -> Product:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def add_category(self, db: Session, db_obj: Product,
                     category: Category) -> List[Category]:
        temp = [*db_obj.categories, category]
        db_obj.categories = temp
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return temp

    def remove_category(self, db: Session, db_obj: Product, category: Category):
        temp = {c.id: c for c in db_obj.categories}
        if temp.get(category.id):
            del temp[category.id]
        temp = [*temp.values()]
        db_obj.categories = temp
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return temp


product_repo = ProductRepository(Product)
