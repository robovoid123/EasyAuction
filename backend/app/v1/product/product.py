from app.schemas.product import ProductCreate, ProductCreateRequest, ProductUpdate
from sqlalchemy.orm import Session

from app.easy_auction.base import Base
from app.crud.product.product import crud_product
from app.easy_auction.product.category import Category
from app.easy_auction.product.inventory import Inventory


class Product(Base):
    def __init__(self, db: Session):
        super().__init__(crud_product, db)
        self.inventory = Inventory(db)
        self.category = Category(db)

    def create(self, obj_in: ProductCreateRequest):
        product_in = ProductCreate(**obj_in)
        db_obj = super().create(product_in)
        inventory = self.inventory.create(
            {'quantity': obj_in.get('quantity')})
        self.add_inventory(db_obj, inventory)
        categories = self.category.get_with_names(obj_in.get('categories'))
        self.add_categories(db_obj, categories)
        return db_obj

    def update(self, db_obj, obj_in):
        product_in = ProductUpdate(**obj_in.dict(exclude_unset=True))
        db_obj = super().update(db_obj, product_in)
        if obj_in.quantity:
            self.update_inventory(db_obj, obj_in.quantity)
        return db_obj

    def add_inventory(self, db_obj, inventory):
        self.crud.add_inventory(db_obj, inventory)

    def update_inventory(self, db_obj, quantity):
        self.inventory.update(db_obj=db_obj.inventory, obj_in={
            'quantity': quantity
        })

    def add_categories(self, db_obj, categories):
        self.crud.add_categories(db_obj, categories)

    def reserve(self, id, quantity):
        db_obj = self.get(id)
        return self.inventory.reserve(db_obj.inventory, quantity)

    def free(self, id, quantity):
        db_obj = self.get(id)
        return self.inventory.free(db_obj.inventory, quantity)
