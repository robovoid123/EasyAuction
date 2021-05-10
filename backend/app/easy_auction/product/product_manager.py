from app.crud.product import product as product_crud
from app.easy_auction.product.product import Product


class ProductManager:
    def get_product(self, db, id):
        db_obj = product_crud.get(db, id)
        if not db_obj:
            """
            product not found
            """
        product = Product(db, id)
        return product

    def create_product(self, db, obj_in, quantity, categories):
        product_creator = Product(db)
        new_product = product_creator.create(obj_in)
        product_creator.add_categories(categories)
        product_creator.add_inventory(quantity)
        return new_product

    def get_multi(self, db, *, skip, limit):
        return product_crud.get_multi(db, skip=skip, limit=limit)


product_manager = ProductManager()
