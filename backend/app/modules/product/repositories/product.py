from typing import List

from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.repository.repository_base import BaseRepository

from app.modules.product.repositories.inventory import inventory_repo
from app.modules.product.repositories.category import category_repo
from app.modules.product.schemas import InventoryCreate, InventoryUpdate, ProductCreate, ProductUpdate
from app.modules.product.models import Product, Inventory
from app.modules.product.models.service_type import ServiceType


class ProductRepository(BaseRepository[Product, ProductCreate, ProductUpdate]):
    def create_with_owner(self, db: Session, obj_in: ProductCreate, owner_id: int) -> Product:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def reserve(self, db: Session, db_obj: Product, quantity: int, service_type: ServiceType) -> Inventory:
        """
        reserve products from inventory to any of the service
        product can be reserved by several services at once but
        only 1 reserve request for each service.
        we can't have 2 different auciton for same product at once
        """
        return inventory_repo.create_reserve(db, db_obj=db_obj.inventory, quantity=quantity, service_type=service_type)

    def unreserve(self, db: Session, db_obj: Product, service_type: ServiceType) -> Inventory:
        """
        return product back to inventory
        if the transaction failed or canceled
        """
        return inventory_repo.cancel_reserve(db, db_obj=db_obj.inventory, service_type=service_type)

    def free(self, db: Session, db_obj: Product, service_type: ServiceType) -> Inventory:
        """
        free after transaction sucessfully complete
        """
        return inventory_repo.free_reserve(db, db_obj=db_obj.inventory, service_type=service_type)

    def create_inventory(self, db: Session, db_obj: Product, quantity: int) -> Inventory:
        """
        inventory keeps track of the product stock and
        from inventory we can reserve product inorder to use
        product in vairous service.
        for eg.:
            if we create auction then we need to reserve a product
            for the auction and if the auction is unsucessful the
            product gets returned back to the inventory.
        """
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

    def remove_categories(self, db: Session, db_obj: Product,
                          category_ids: List[int]):
        categories = list(filter(lambda c: c.id not in category_ids, db_obj.categories))
        db_obj.categories = categories
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return categories

    def add_categories(self, db: Session, db_obj: Product, category_ids: List[int]):
        categories = category_repo.get_multi_with_ids(db, ids=category_ids)
        db_obj.categories = categories
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return categories

    def get_reserves(self, db: Session, db_obj: Product):
        return db_obj.inventory.reserve


product_repo = ProductRepository(Product)
