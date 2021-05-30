from sqlalchemy.orm import Session

from app.modules.product.repositories import category_repo, product_repo
from app.modules.product.models import Product, Category
from app.modules.product.schemas import ProductCreate, CategoryCreate

from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def create_random_product(db: Session) -> Product:
    name = random_lower_string()
    desc = random_lower_string()
    owner = create_random_user(db)

    return product_repo.create_with_user(db, obj_in=ProductCreate(
        name=name, description=desc
    ), owner_id=owner.id)


def create_random_category(db: Session) -> Category:
    name = random_lower_string()
    desc = random_lower_string()

    return category_repo.create(db, obj_in=CategoryCreate(
        name=name, description=desc
    ))
