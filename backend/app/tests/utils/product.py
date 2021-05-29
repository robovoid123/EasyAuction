import random
from sqlalchemy.orm import Session

from app.modules.product.repositories import category_repo, product_repo
from app.modules.product.models import Conditions, Product as ProductModel
from app.modules.product.schemas import ProductCreate

from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


CATEGORY_LIST = ["books", "electronics", "fashions"]


def get_categories(db: Session):

    cat_list = category_repo.get_with_names(db, CATEGORY_LIST)

    names = [c.name for c in cat_list]
    if names != CATEGORY_LIST:
        cat_list = [category_repo.create(
            db, obj_in={"name": name}) for name in CATEGORY_LIST]
    return cat_list


def random_condition():
    return random.choices(list(Conditions))[0]


def create_random_product(db: Session) -> ProductModel:
    user = create_random_user(db)
    quantity = random.randint(1, 100)
    categories = get_categories(db)
    category_ids = [c.id for c in categories]
    name = random_lower_string()
    desc = random_lower_string()
    condition = random_condition()
    prod_obj = ProductCreate(
        name=name,
        description=desc,
        condition=condition,
    )

    db_obj = product_repo.create_with_owner(db, obj_in=prod_obj, owner_id=user.id)
    product_repo.create_inventory(db, db_obj=db_obj, quantity=quantity)
    product_repo.add_categories(db, db_obj=db_obj, category_ids=category_ids)
    return db_obj
