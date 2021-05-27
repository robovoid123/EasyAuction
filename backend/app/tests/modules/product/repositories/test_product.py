from random import randint
from sqlalchemy.orm.session import Session

from app.tests.utils.user import create_random_user
from app.modules.product.repositories import product_repo
from app.modules.product.schemas import ProductCreate, ProductUpdate
from app.modules.product.models import ServiceType, service_type

from app.tests.utils.product import (random_condition,
                                     get_categories,
                                     create_random_product)
from app.tests.utils.utils import random_lower_string


def test_create_complete_product(db: Session):
    user = create_random_user(db)
    quantity = randint(1, 100)
    categories = get_categories(db)
    category_ids = [c.id for c in categories]
    name = random_lower_string()
    desc = random_lower_string()
    condition = random_condition()
    prod_obj = ProductCreate(
        name=name,
        owner_id=user.id,
        description=desc,
        condition=condition,
    )
    product = product_repo.create_complete(db, obj_in=prod_obj, owner_id=user.id,
                                           quantity=quantity, category_ids=category_ids)

    db_obj = product_repo.get(db, id=product.id)

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

    db_obj = product_repo.get(db, id=prod_db.id)

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
    product_repo.update_complete(db, db_obj=prod_db, obj_in=update_obj,
                                 quantity=quantity)
    db_obj = product_repo.get(db, prod_db.id)

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
    service_type = ServiceType.AUCTION

    product_repo.reserve(db, db_obj=prod_db, quantity=reserve_quantity,
                         service_type=service_type)
    db_obj = product_repo.get(db, prod_db.id)

    assert db_obj
    assert db_obj.inventory.quantity == final_quantity
    assert db_obj.inventory.reserve


def test_unreserve_product(db: Session):
    prod_db = create_random_product(db)
    service_type = ServiceType.AUCTION

    prev_quantity = prod_db.inventory.quantity
    reserve_quantity = int(prev_quantity - prev_quantity / 2)
    final_quantity = prev_quantity - reserve_quantity
    product_repo.reserve(db, db_obj=prod_db, quantity=final_quantity,
                         service_type=service_type)

    assert prod_db.inventory.reserve

    prod_db = product_repo.get(db, prod_db.id)

    product_repo.unreserve(db, db_obj=prod_db, service_type=service_type)
    db_obj = product_repo.get(db, prod_db.id)

    assert db_obj
    assert db_obj.inventory.quantity
    assert not db_obj.inventory.reserve


def test_free_product(db: Session):
    prod_db = create_random_product(db)
    service_type = ServiceType.AUCTION

    prev_quantity = prod_db.inventory.quantity
    reserve_quantity = int(prev_quantity - prev_quantity / 2)
    final_quantity = prev_quantity - reserve_quantity
    product_repo.reserve(db, db_obj=prod_db, quantity=final_quantity,
                         service_type=service_type)

    assert prod_db.inventory.reserve

    prod_db = product_repo.get(db, prod_db.id)

    product_repo.free(db, db_obj=prod_db, service_type=service_type)

    assert prod_db.inventory.quantity == final_quantity
    assert not prod_db.inventory.reserve
