from datetime import datetime

from app.crud.product import product
from app.crud.category import category
from app.crud.inventory import inventory

from app.schemas.product import InventoryCreate, InventoryUpdate


class Product:
    def __init__(self, db, id=None):
        self.db = db
        self.db_obj = None
        if id:
            self.db_obj = product.get(db, id)

    def get(self):
        return self.db_obj

    def create(self, obj_in):
        new_product = product.create(self.db, obj_in=obj_in)
        self.db_obj = new_product
        return new_product

    def update(self, *, obj_in):
        return product.update(self.db, db_obj=self.db_obj, obj_inj=obj_in)

    def remove(self):
        return product.remove(self.db, id=self.db_obj.id)

    def create_inventory(self, quantity):
        obj_in = InventoryCreate(quantity=quantity)
        return inventory.create_with_date(self.db, obj_in, datetime.now())

    def update_inventory(self, quantity):
        db_obj = self.db_obj.inventory
        obj_in = InventoryUpdate(quantity=quantity)
        return inventory.update(self.db, db_obj=db_obj, obj_in=obj_in)

    def add_inventory(self, quantity):
        new_inventory = self.create_inventory(quantity)
        self.db_obj.inventory = new_inventory
        return new_inventory

    def add_category(self, name):
        cat = category.get_with_name(self.db, name)
        if cat:
            self.db_obj.categories.append(cat)
        return cat

    def add_categories(self, names):
        cat_list = []
        for name in names:
            cat_list.append(self.add_category(
                db=self.db, name=name))
        self.db.add(self.db_obj)
        self.db.commit()
        self.db.refresh(self.db_obj)
        return cat_list

    def update_categories(self, categories):
        pass
