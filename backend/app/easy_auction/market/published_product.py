from fastapi import HTTPException
from app.crud.published_product import published_product as crud
from app.crud.buy_history import buy_history as buy_crud
from app.easy_auction import product_manager


class PublishedProduct:
    def __init__(self, db, id=None, db_obj=None):
        self.db = db
        if id:
            """
            get from db
            """
        elif db_obj:
            self.db_obj = db_obj

        if self.db_obj:
            product_db_obj = self.db_obj.product
            self._product = product_manager.populate_from_obj(db, product_db_obj)

    """
    properties related to the class
    """
    @property
    def price(self): return self.db_obj.price

    @property
    def product(self): return self._product

    @property
    def shop(self): return self.db_obj.shop

    @property
    def quantity(self):
        if self.db_obj.quantity <= 0:
            raise HTTPException(
                status_code=400,
                detail="product out of stock"
            )
        return self.db_obj.quantity

    @classmethod
    def create(cls, db, obj_in):
        product = product_manager.get_product(db, obj_in.product_id)
        product.reserve(obj_in.quantity)
        db_obj = crud.create(db, obj_in=obj_in)
        return cls(db, db_obj=db_obj)

    def get(self):
        return self.db_obj

    def update(self, obj_in):
        return crud.update(self.db, db_obj=self.db_obj, obj_in=obj_in)

    def remove(self):
        self.product.free(self.db_obj.quantity)
        return crud.remove(self.db, id=self.db_obj.id)

    def buy(self, quantity, buyer_id):
        if quantity > self.quantity:
            # TODO: not enough product to sell
            pass
        self.update({
            'quantity': self.quantity - quantity,
        })

        obj = {
            'quantity': quantity,
            'product_id': self.db_obj.id,
            'buyer_id': buyer_id
        }
        buy_crud.create(self.db, obj_in=obj)

    def add_to_shop(self, shop_id):
        self.update({'shop_id': shop_id})

    def remove_from_shop(self, shop_id):
        self.update({'shop_id': None})
