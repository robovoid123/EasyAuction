from typing import List, Optional
from fastapi.exceptions import HTTPException

from sqlalchemy.orm import Session
from app.crud.base import CRUDBase

from app.crud.product.inventory import crud_inventory
from app.crud.product.category import crud_category
from app.schemas.product import InventoryCreate, InventoryUpdate, ProductCreate, ProductUpdate
from app.models.product import Product, Inventory, Category


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    def create_complete(self, db: Session, obj_in: ProductCreate,
                        quantity: int, categories: List[str]) -> Product:
        db_obj = self.create(db, obj_in=obj_in)
        inven_obj = InventoryCreate(quantity=quantity)
        inventory = crud_inventory.create(db, obj_in=inven_obj)
        db_obj.inventory = inventory
        categories = crud_category.get_with_names(db, categories)
        db_obj.categories = categories
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_complete(self, db: Session, db_obj: Product,
                        obj_in: ProductUpdate, quantity: Optional[int] = None) -> Product:

        db_obj = self.update(db, db_obj=db_obj, obj_in=obj_in)
        if quantity:
            inven_obj = InventoryUpdate(quantity=quantity)
            crud_inventory.update(db, db_obj=db_obj.inventory, obj_in=inven_obj)
        return db_obj

    def reserve(self, db: Session, id: int, quantity: int) -> None:
        db_obj = self.get(db, id)
        inventory: Inventory = db_obj.inventory
        if inventory.quantity < quantity:
            raise HTTPException(status_code=400,
                                detail="cannot reserve not enough product in inventory")
        inven_obj = InventoryUpdate(quantity=inventory.quantity-quantity)
        crud_inventory.update(db, db_obj=inventory, obj_in=inven_obj)

    def free(self, db: Session, id: int, quantity: int) -> None:
        db_obj = self.get(db, id)
        inventory: Inventory = db_obj.inventory
        inven_obj = InventoryUpdate(quantity=inventory.quantity+quantity)
        crud_inventory.update(db, db_obj=inventory, obj_in=inven_obj)


crud_product = CRUDProduct(Product)
