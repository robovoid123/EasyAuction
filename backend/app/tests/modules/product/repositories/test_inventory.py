from random import randint
from sqlalchemy.orm.session import Session

from app.tests.utils.user import create_random_user
from app.modules.product.repositories import inventory_repo
from app.modules.product.schemas import ProductCreate, ProductUpdate
from app.modules.product.models import ServiceType, service_type

from app.tests.utils.product import (random_condition,
                                     get_categories,
                                     create_random_product)
from app.tests.utils.utils import random_lower_string


def test_increment_quantity(db: Session):
    prod_db = create_random_product(db)
    prev_quantity = prod_db.inventory.quantity
    quantity = randint(1, 100)
    inven = inventory_repo.increment_quantity(
        db, db_obj=prod_db.inventory, quantity=quantity)

    assert inven.quantity == prev_quantity + quantity


def test_decrement_quantity(db: Session):
    prod_db = create_random_product(db)
    prev_quantity = prod_db.inventory.quantity
    quantity = prev_quantity
    while quantity >= prev_quantity:
        quantity = randint(1, 100)
    inven = inventory_repo.decrement_quantity(
        db, db_obj=prod_db.inventory, quantity=quantity)

    assert inven.quantity == prev_quantity - quantity


def test_create_reserve(db: Session):
    prod_db = create_random_product(db)
    prev_quantity = prod_db.inventory.quantity
    quantity = prev_quantity
    while quantity >= prev_quantity:
        quantity = randint(1, 100)

    service_type = ServiceType.AUCTION
    inventory_repo.create_reserve(db, db_obj=prod_db.inventory,
                                  quantity=quantity, service_type=service_type)

    db.refresh(prod_db)
    assert prod_db.inventory.reserve
    assert prod_db.inventory.reserve[0].service_type == service_type
    assert prod_db.inventory.reserve[0].quantity == quantity
    assert prod_db.inventory.quantity == prev_quantity - quantity


def test_cancel_reserve(db: Session):
    prod_db = create_random_product(db)
    prev_quantity = prod_db.inventory.quantity
    quantity = prev_quantity
    while quantity >= prev_quantity:
        quantity = randint(1, 100)

    service_type = ServiceType.AUCTION
    inventory_repo.create_reserve(db, db_obj=prod_db.inventory,
                                  quantity=quantity, service_type=service_type)
    db.refresh(prod_db)
    assert prod_db.inventory.reserve
    assert prod_db.inventory.reserve[0].service_type == service_type
    assert prod_db.inventory.reserve[0].quantity == quantity

    inventory_repo.cancel_reserve(db, db_obj=prod_db.inventory, service_type=service_type)

    assert not prod_db.inventory.reserve
    assert prod_db.inventory.quantity == prev_quantity


def test_free_reserve(db: Session):
    prod_db = create_random_product(db)
    prev_quantity = prod_db.inventory.quantity
    quantity = prev_quantity
    while quantity >= prev_quantity:
        quantity = randint(1, 100)

    service_type = ServiceType.AUCTION
    inventory_repo.create_reserve(db, db_obj=prod_db.inventory,
                                  quantity=quantity, service_type=service_type)
    db.refresh(prod_db)
    assert prod_db.inventory.reserve
    assert prod_db.inventory.reserve[0].service_type == service_type
    assert prod_db.inventory.reserve[0].quantity == quantity

    inventory_repo.free_reserve(db, db_obj=prod_db.inventory, service_type=service_type)

    assert not prod_db.inventory.reserve
    assert prod_db.inventory.quantity == prev_quantity - quantity
