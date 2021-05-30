from app.modules.product.models.product import Product
from sqlalchemy.orm.session import Session

from app.tests.utils.utils import random_lower_string
from app.tests.utils.user import create_random_user
from app.tests.utils.product import create_random_category, create_random_product
from app.modules.product.schemas import (ProductCreate, ProductUpdate)
from app.modules.product.repositories import product_repo


def test_create_with_user_product(db: Session):
    name = random_lower_string()
    desc = random_lower_string()
    owner = create_random_user(db)

    product = product_repo.create_with_user(db, obj_in=ProductCreate(
        name=name, description=desc
    ), owner_id=owner.id)

    db_obj = product_repo.get(db, id=product.id)

    assert db_obj
    assert db_obj.name == name
    assert db_obj.description == desc
    assert db_obj.owner_id == owner.id


def test_create_product(db: Session):
    name = random_lower_string()
    desc = random_lower_string()

    product = product_repo.create(db, obj_in=ProductCreate(
        name=name, description=desc
    ))

    db_obj = product_repo.get(db, id=product.id)

    assert db_obj
    assert db_obj.name == name
    assert db_obj.description == desc


def test_update_product(db: Session):
    name = random_lower_string()
    desc = random_lower_string()

    product = product_repo.create(db, obj_in=ProductCreate(
        name=name, description=desc
    ))

    new_name = random_lower_string()
    new_desc = random_lower_string()
    new_product = product_repo.update(db, db_obj=product, obj_in=ProductUpdate(
        name=new_name,
        description=new_desc
    ))

    db_obj = product_repo.get(db, id=product.id)

    assert db_obj.name == new_name
    assert db_obj.description == new_desc


def test_delete_product(db: Session):
    name = random_lower_string()
    desc = random_lower_string()

    product = product_repo.create(db, obj_in=ProductCreate(
        name=name, description=desc
    ))

    product_repo.remove(db, id=product.id)

    db_obj = product_repo.get(db, id=product.id)

    assert not db_obj


def test_add_category(db: Session):
    product = create_random_product(db)

    cat1 = create_random_category(db)

    product_repo.add_category(db, db_obj=product, category=cat1)

    db_obj = product_repo.get(db, id=product.id)

    assert db_obj.categories[0].name == cat1.name


def test_remove_category(db: Session):
    product = create_random_product(db)

    cat1 = create_random_category(db)

    product_repo.add_category(db, db_obj=product, category=cat1)

    db_obj = product_repo.get(db, id=product.id)

    assert db_obj.categories[0].name == cat1.name

    db_obj = product_repo.remove_category(db, db_obj=product, category=cat1)
    db_obj = product_repo.get(db, id=product.id)

    assert not db_obj.categories
