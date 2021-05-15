from app.crud.base import CRUDBase
from app.schemas.product import ProductCreate, ProductUpdate
from app.models.product import Product


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    def add_inventory(self, db_obj, inventory):
        db_obj.inventory = inventory
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def add_categories(self, db_obj, categories):
        db_obj.categories = categories
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj


crud_product = CRUDProduct(Product)
