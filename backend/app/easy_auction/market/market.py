from app.easy_auction.market.published_product import PublishedProduct
from app.easy_auction.market.shop import Shop
from app.crud.published_product import published_product as product_crud
from app.crud.shop import shop as shop_crud

"""
market is the place where product can be sold
and shops can be opened
"""


class Market:
    def get_shop(self, db, id):
        db_obj = shop_crud.get(db, id)
        if db_obj:
            return Shop(db, db_obj=db_obj)

    def create_shop(self, db, obj_in):
        return Shop.create(db, obj_in)

    def get_shops(self, db, *, skip, limit):
        return product_crud.get_multi(db, skip=skip, limit=limit)

    def get_published_product(self, db, id):
        db_obj = product_crud.get(db, id)
        if db_obj:
            return PublishedProduct(db, db_obj=db_obj)

    def get_published_products(self, db, *, skip, limit):
        return product_crud.get_multi(db, skip=skip, limit=limit)

    def publish_product(self, db, obj_in):
        return PublishedProduct.create(db, obj_in=obj_in)

    def unpublish_product(self, db, id):
        product = self.get_published_product(db, id)
        return product.remove()


market = Market()
