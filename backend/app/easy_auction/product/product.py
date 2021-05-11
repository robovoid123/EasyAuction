from datetime import datetime
from typing import List, Optional

from app.crud.product import product
from app.crud.category import category
from app.crud.inventory import inventory

from app.schemas.product import InventoryCreate, InventoryUpdate
from app.models import product as prm


class Product:
    def __init__(self, db, id=None, db_obj=None):
        self.db = db
        self.db_obj = None
        if id:
            self.db_obj = product.get(db, id)
        if db_obj:
            self.db_obj = db_obj

    # TODO: implement all the property of product

    @property
    def inventory(self):
        return self.db_obj.inventory

    @property
    def categories(self):
        return self.db_obj.categories

    @property
    def owner(self):
        return self.db_obj.owner

    @classmethod
    def create(cls, db, obj_in):
        db_obj = product.create(db, obj_in=obj_in)
        return cls(db, db_obj=db_obj)

    def get(self) -> Optional[prm.Product]:
        return self.db_obj

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
        self.db.add(self.db_obj)
        self.db.commit()
        self.db.refresh(self.db_obj)
        return self.db_obj.inventory

    def add_category(self, name):
        cat = category.get_with_name(self.db, name)
        if cat:
            self.db_obj.categories.append(cat)
            self.db.add(self.db_obj)
            self.db.commit()
            self.db.refresh(self.db_obj)
            return cat

    def add_categories(self, names: List[str]):
        categories = category.get_with_names(self.db, names)
        if categories:
            [self.db_obj.categories.append(cat) for cat in categories]
            self.db.add(self.db_obj)
            self.db.commit()
            self.db.refresh(self.db_obj)
            return self.db_obj.categories

    # TODO: should take complete categories of present auction
    def update_categories(self, categories):
        pass
