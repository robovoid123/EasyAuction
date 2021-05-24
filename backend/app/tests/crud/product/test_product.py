from random import randint
from sqlalchemy.orm.session import Session

from app.tests.utils.user import create_random_user
from app.crud.product.product import crud_product
from app.schemas.product import ProductCreate, ProductUpdate

from app.tests.utils.product import (random_condition,
                                     get_categories,
                                     create_random_product)
from app.tests.utils.utils import random_lower_string


def test_create_complete_product(db: Session):
    user = create_random_user(db)
    quantity = randint(1, 100)
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
    product = crud_product.create_complete(db, obj_in=prod_obj,
                                           quantity=quantity, categories=category_names)

    db_obj = crud_product.get(db, id=product.id)

    assert db_obj == product
    assert db_obj.owner_id == user.id
    assert db_obj.inventory
    assert db_obj.inventory.quantity == quantity
    assert db_obj.categories
    assert db_obj.categories == categories
    assert db_obj.name == name
    assert db_obj.description == desc
    assert db_obj.condition == condition


def test_get_product(db: Session):
    prod_db = create_random_product(db)

    db_obj = crud_product.get(db, id=prod_db.id)

    assert db_obj == prod_db
    assert db_obj.owner_id == prod_db.owner_id
    assert db_obj.inventory
    assert db_obj.categories


def test_update_complete_product(db: Session):
    prod_db = create_random_product(db)
    quantity = randint(1, 100)
    name = random_lower_string()
    desc = random_lower_string()
    condition = random_condition()

    update_obj = ProductUpdate(
        name=name,
        description=desc,
        condition=condition
    )
    crud_product.update_complete(db, db_obj=prod_db, obj_in=update_obj,
                                 quantity=quantity)
    db_obj = crud_product.get(db, prod_db.id)

    assert db_obj
    assert db_obj.name == name
    assert db_obj.description == desc
    assert db_obj.condition == condition
    assert db_obj.inventory.quantity == quantity
    assert db_obj.categories == prod_db.categories


def test_delete_product(db: Session):
    pass


def test_reserve_product(db: Session):
    prod_db = create_random_product(db)
    prev_quantity = prod_db.inventory.quantity
    reserve_quantity = int(prev_quantity - prev_quantity / 2)
    final_quantity = prev_quantity - reserve_quantity

    crud_product.reserve(db, prod_db.id, quantity=reserve_quantity)
    db_obj = crud_product.get(db, prod_db.id)

    assert db_obj
    assert db_obj.inventory.quantity == final_quantity


def test_free_product(db: Session):
    prod_db = create_random_product(db)
    prev_quantity = prod_db.inventory.quantity
    free_quantity = int(prev_quantity + prev_quantity / 2)
    final_quantity = prev_quantity + free_quantity

    crud_product.free(db, prod_db.id, quantity=free_quantity)
    db_obj = crud_product.get(db, prod_db.id)

    assert db_obj
    assert db_obj.inventory.quantity == final_quantity
