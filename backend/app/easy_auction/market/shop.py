from app.crud.shop import shop as crud
from app.easy_auction import market


class Shop:
    def __init__(self, db, id=None, db_obj=None):
        self.db = db
        if id:
            """
            get from db
            """
        elif db_obj:
            self.db_obj = db_obj

    """
    properties related to the class
    """
    @property
    def name(self): return self.db_obj.price

    @property
    def description(self): return self._product

    @property
    def products(self): return self.db_obj.shop

    @property
    def owner(self): return self.db_obj.owner

    @classmethod
    def create(cls, db, obj_in):
        db_obj = crud.create(db, obj_in=obj_in)
        return cls(db, db_obj=db_obj)

    def get(self):
        return self.db_obj

    def update(self, obj_in):
        return crud.update(self.db, db_obj=self.db_obj, obj_in=obj_in)

    def remove(self):
        return crud.remove(self.db, id=self.db_obj.id)

    def get_products(self):
        return self.db_obj.products

    def get_product(self, product_id):
        product = market.get_published_product(self.db, id=product_id)
        return product.get()

    def add_product(self, product_id):
        product = market.get_published_product(self.db, id=product_id)
        return product.add_to_shop(self.db_obj.id)

    def remove_product(self, product_id):
        product = market.get_published_product(self.db, id=product_id)
        return product.remove_from_shop(self.db_obj.id)
