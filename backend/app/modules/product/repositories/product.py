from typing import List

from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from sqlalchemy.sql.roles import DMLTableRole

from app.repository.repository_base import BaseRepository

from app.modules.product.schemas import ProductCreate, ProductUpdate
from app.modules.product.models import Product, Category
from app.modules.utils.models import Image


class ProductRepository(BaseRepository[Product, ProductCreate, ProductUpdate]):

    def get_multi_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ):
        return db.query(self.model).filter(self.model.owner_id == user_id).offset(skip).limit(limit).all()

    def create_with_user(self, db: Session, *,
                         obj_in: ProductCreate, owner_id: int) -> Product:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def add_image(self, db: Session, db_obj: Product, image: Image) -> List[Image]:
        db_obj.images.append(image)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj.images

    def add_images(self, db: Session, db_obj: Product, images: List[Image]) -> List[Image]:
        db_obj.images = [*db_obj.images, *images]
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj.images

    def remove_image(self, db: Session, db_obj: Product, image: Image):
        db_obj.images = list(filter(lambda img: img.url != image.url, db_obj.images))
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

    def add_category(self, db: Session, db_obj: Product,
                     category: Category) -> List[Category]:
        db_obj.categories.append(category)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return category

    def add_categories(self, db: Session, db_obj: Product,
                       categories: List[Category]) -> List[Category]:
        temp = [*db_obj.categories, *categories]
        db_obj.categories = temp
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return temp

    def remove_category(self, db: Session, db_obj: Product, category: Category):
        db_obj.categories = list(filter(lambda c: c.id != category.id, db_obj.categories))
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)


product_repo = ProductRepository(Product)
