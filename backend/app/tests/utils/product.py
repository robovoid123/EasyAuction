import random
from sqlalchemy.orm import Session

from app.crud.product.category import crud_category
from app.models.product import Conditions, Product as ProductModel

from app.tests.utils.user import create_random_user
from app.crud.product.product import crud_product
from app.schemas.product import ProductCreate

from app.tests.utils.utils import random_lower_string


CATEGORY_LIST = ["books", "electronics", "fashions"]


def get_categories(db: Session):

    cat_list = crud_category.get_with_names(db, CATEGORY_LIST)

    names = [c.name for c in cat_list]
    if names != CATEGORY_LIST:
        cat_list = [crud_category.create(
            db, obj_in={"name": name}) for name in CATEGORY_LIST]
    return cat_list


def random_condition():
    return random.choices(list(Conditions))[0]


def create_random_product(db: Session) -> ProductModel:
    user = create_random_user(db)
    quantity = random.randint(1, 100)
    categories = get_categories(db)
    category_names = [c.name for c in categories]
    name = random_lower_string()
    desc = random_lower_string()
    condition = random_condition()
    prod_obj = ProductCreate(
        name=name,
        owner_id=user.id,
        description=desc,
        condition=condition,
    )
    return crud_product.create_complete(db, obj_in=prod_obj,
                                        quantity=quantity, categories=category_names)
