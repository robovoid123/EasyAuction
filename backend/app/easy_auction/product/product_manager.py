from app.crud.product import product as product_crud
from app.easy_auction.product.product import Product


class ProductManager:
    def get_product(self, db, id) -> Product:
        db_obj = product_crud.get(db, id)
        if db_obj:
            return self.populate_from_obj(db, db_obj)

    def populate_from_obj(self, db, db_obj) -> Product:
        return Product(db, db_obj=db_obj)

    def create_product(self, db, obj_in, quantity, categories) -> Product:
        new_product = Product.create(db, obj_in=obj_in)
        new_product.add_categories(categories)
        new_product.add_inventory(quantity)

        return new_product

    def get_multi(self, db, *, skip, limit):
        return product_crud.get_multi(db, skip=skip, limit=limit)


product_manager = ProductManager()
