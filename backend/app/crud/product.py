from typing import List
from datetime import datetime
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.schemas import product as cp
from app.models.product import Product, Inventory, Category, CategoryList


class CRUDProduct(CRUDBase[Product, cp.ProductCreate, cp.ProductUpdate]):

    def create_new(self,
                   *,
                   db: Session,
                   obj_in: cp.ProductCreate,
                   quantity: int,
                   categories: List[CategoryList]) -> Product:

        new_product = product.create(db=db,
                                     obj_in=obj_in,
                                     commit=False)
        new_product = product.add_inventory(
            db=db, db_obj=new_product, quantity=quantity, commit=False)
        new_product = product.add_categories(db=db,
                                             categories=categories,
                                             db_obj=new_product, commit=False)
        db.commit()
        db.refresh(new_product)
        return new_product

    def update_all(self,
                   *,
                   db: Session,
                   db_obj: Product,
                   obj_in: cp.ProductUpdate,
                   quantity: int,
                   categories: List[CategoryList]) -> Product:

        if quantity is not None:
            product.update_inventory(db=db,
                                     db_obj=db_obj,
                                     quantity=quantity,
                                     )
        if categories:
            product.add_categories(db=db,
                                   db_obj=db_obj,
                                   categories=categories)

        return product.update(db=db, db_obj=db_obj, obj_in=obj_in)

    def create_inventory(self,
                         *,
                         db: Session,
                         quantity: int,
                         commit=True) -> Inventory:
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
                         db_obj: Product,
                         quantity: int,
                         commit=True
                         ) -> Product:

        db_obj.inventory.quantity = quantity
        if commit:
            db.commit()
            db.refresh(db_obj)
        return db_obj

    def add_inventory(self,
                      db: Session,
                      db_obj: Product,
                      quantity: int,
                      commit=True) -> Product:
        new_inventory = self.create_inventory(db=db, quantity=quantity, commit=commit)
        db_obj.inventory = new_inventory
        return db_obj

    def add_category(
            self,
            *,
            db: Session,
            db_obj: Product,
            category: CategoryList,
            commit=True) -> Product:

        category = Category(category=category)
        db_obj.categories.append(category)
        if commit:
            db.commit()
            db.refresh(db_obj)
        return db_obj

    def add_categories(
            self,
            *,
            db: Session,
            db_obj: Product,
            categories: List[CategoryList],
            commit=True):

        for category in categories:
            db_obj = self.add_category(db=db,
                                       category=category,
                                       db_obj=db_obj,
                                       commit=False)
        db.add(db_obj)
        if commit:
            db.commit()
            db.refresh(db_obj)
        return db_obj


product = CRUDProduct(Product)
