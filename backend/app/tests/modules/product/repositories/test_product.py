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


def create_random_product_without_inventory(db: Session):
    user = create_random_user(db)
    name = random_lower_string()
    desc = random_lower_string()
    condition = random_condition()

    obj_in = ProductCreate(name=name, description=desc, condition=condition)
    return product_repo.create_with_owner(db, obj_in=obj_in, owner_id=user.id)


def test_create_with_owner(db: Session):
    user = create_random_user(db)
    name = random_lower_string()
    desc = random_lower_string()
    condition = random_condition()

    obj_in = ProductCreate(name=name, description=desc, condition=condition)
    db_obj = product_repo.create_with_owner(db, obj_in=obj_in, owner_id=user.id)

    assert db_obj
    assert db_obj.id
    assert db_obj.name == name
    assert db_obj.description == desc
    assert db_obj.condition == condition


def test_create_inventory(db: Session):
    db_obj = create_random_product_without_inventory(db)

    quantity = randint(1, 100)

    inven = product_repo.create_inventory(db, db_obj=db_obj, quantity=quantity)
    db.refresh(db_obj)

    assert inven
    assert inven.id
    assert db_obj.inventory
    assert db_obj.inventory.id
    assert db_obj.inventory.quantity == quantity


def test_update_inventory(db: Session):
    db_obj = create_random_product_without_inventory(db)

    quantity = randint(1, 100)
    inven = product_repo.create_inventory(db, db_obj=db_obj, quantity=quantity)
    assert inven.quantity == quantity
    old_update_at = inven.updated_at

    db.refresh(db_obj)

    new_quantity = randint(1, 100)
    new_inven = product_repo.update_inventory(db, db_obj=db_obj, quantity=new_quantity)
    assert new_inven.quantity == new_quantity
    assert new_inven.updated_at > old_update_at


def test_add_categories(db: Session):
    db_obj = create_random_product_without_inventory(db)
    categories = get_categories(db)
    category_ids = [c.id for c in categories]

    product_repo.add_categories(db, db_obj=db_obj, category_ids=category_ids)
    db.refresh(db_obj)
    assert db_obj.categories
    assert db_obj.categories == categories


def test_remove_categories(db: Session):
    db_obj = create_random_product_without_inventory(db)
    categories = get_categories(db)
    category_ids = [c.id for c in categories]

    product_repo.add_categories(db, db_obj=db_obj, category_ids=category_ids)
    db.refresh(db_obj)
    assert db_obj.categories == categories

    product_repo.remove_categories(db, db_obj=db_obj, category_ids=category_ids)

    db.refresh(db_obj)
    assert db_obj.categories not in categories


def test_get_product(db: Session):
    prod_db = create_random_product(db)

    db_obj = product_repo.get(db, id=prod_db.id)

    assert db_obj == prod_db
    assert db_obj.owner_id == prod_db.owner_id
    assert db_obj.inventory
    assert db_obj.categories


def test_update_product(db: Session):
    db_obj = create_random_product_without_inventory(db)
    name = random_lower_string()
    desc = random_lower_string()
    condition = random_condition()

    update_obj = ProductUpdate(
        name=name,
        description=desc,
        condition=condition
    )
    product_repo.update(db, db_obj=db_obj, obj_in=update_obj)

    db.refresh(db_obj)

    assert db_obj
    assert db_obj.name == name
    assert db_obj.description == desc
    assert db_obj.condition == condition


def test_delete_product(db: Session):
    pass
