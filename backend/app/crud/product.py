from typing import List
from datetime import datetime
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.schemas import product as cp
from app.models.product import Product, Inventory, Category, CategoryList


class CRUDProduct(CRUDBase[Product, cp.ProductCreate, cp.ProductUpdate]):
    def create_inventory(self, *, db: Session, quantity: int, commit=True):
        restocked_at = datetime.now()
        inventory = Inventory(quantity=quantity, restocked_at=restocked_at)
        db.add(inventory)
        if commit:
            db.commit()
            db.refresh(inventory)
        return inventory

    def update_inventory(self,
                         *,
                         db: Session,
                         product_db: Product,
                         quantity: int,
                         commit=True
                         ):

        product_db.inventory.quantity = quantity
        if commit:
            db.commit()
            db.refresh(product_db)
        return product_db.inventory

    def add_category(
            self,
            *,
            db: Session,
            category: CategoryList,
            product_id: int,
            commit=True):

        category = Category(category=category,
                            product_id=product_id)
        db.add(category)
        if commit:
            db.commit()
            db.refresh(category)
        return category

    def add_categories(
            self,
            *,
            db: Session,
            categories: List[CategoryList],
            product_id: int,
            commit=True):

        def add_cat(category):
            return self.add_category(db=db,
                                     category=category,
                                     product_id=product_id,
                                     commit=False)

        categories = [add_cat(category) for category in categories]
        if commit:
            db.commit()
        return categories


product = CRUDProduct(Product)
