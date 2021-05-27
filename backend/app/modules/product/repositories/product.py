from app.modules.product.models import service_type
from app.modules.product.models.service_type import ServiceType
from typing import List, Optional
from fastapi.exceptions import HTTPException

from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.repository.repository_base import BaseRepository

from app.modules.product.repositories.inventory import inventory_repo
from app.modules.product.repositories.category import category_repo
from app.modules.product.schemas import InventoryCreate, InventoryUpdate, ProductCreate, ProductUpdate
from app.modules.product.models import Product, Inventory, Category


class ProductRepository(BaseRepository[Product, ProductCreate, ProductUpdate]):
    def create_with_owner(self, db: Session, obj_in: ProductCreate, owner_id: int) -> Product:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_complete(self, db: Session, obj_in: ProductCreate, owner_id: int,
                        quantity: int, category_ids: List[int] = None) -> Product:
        db_obj = self.create_with_owner(db, obj_in=obj_in, owner_id=owner_id)
        inventory = self.create_inventory(db, db_obj=db_obj, quantity=quantity)
        if category_ids:
            categories = self.add_categories(db, db_obj=db_obj, category_ids=category_ids)
        return db_obj

    def update_complete(self, db: Session, db_obj: Product,
                        obj_in: ProductUpdate, quantity: Optional[int] = None) -> Product:

        db_obj = self.update(db, db_obj=db_obj, obj_in=obj_in)
        if quantity:
            self.update_inventory(db, db_obj=db_obj, quantity=quantity)
        return db_obj

    def reserve(self, db: Session, db_obj: Product, quantity: int, service_type: ServiceType) -> Inventory:
        """
        reserve products from inventory
        """
        return inventory_repo.create_reserve(db, db_obj=db_obj.inventory, quantity=quantity, service_type=service_type)

    def unreserve(self, db: Session, db_obj: Product, service_type: ServiceType) -> Inventory:
        """
        return product back to inventory
        """
        return inventory_repo.cancel_reserve(db, db_obj=db_obj.inventory, service_type=service_type)

    def free(self, db: Session, db_obj: Product, service_type: ServiceType) -> Inventory:
        """
        free after transaction sucessfully complete
        """
        return inventory_repo.free_reserve(db, db_obj=db_obj.inventory, service_type=service_type)

    def get_inventory(self, db: Session, id: int): pass

    def create_inventory(self, db: Session, db_obj: Product, quantity: int):
        obj_in = InventoryCreate(quantity=quantity)
        inventory = inventory_repo.create(db, obj_in=obj_in)
        db_obj.inventory = inventory
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return inventory

    def update_inventory(self, db: Session, db_obj: Product, quantity: int):
        obj_in = InventoryUpdate(quantity=quantity)
        return inventory_repo.update(db, db_obj=db_obj.inventory, obj_in=obj_in)

    def get_category(self, db: Session, db_obj: Product): pass
    def get_all_categories(self, db: Session, db_obj: Product): pass
    def add_category(self, db: Session, db_obj: Product, category_id: int): pass

    def add_categories(self, db: Session, db_obj: Product, category_ids: List[int]):
        categories = category_repo.get_multi_with_ids(db, ids=category_ids)
        db_obj.categories = categories
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return categories

    def remove_category(self, db: Session, db_obj: Product, category_id: int): pass


product_repo = ProductRepository(Product)
