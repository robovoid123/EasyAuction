from sqlalchemy.orm import Session

from app.tests.utils.utils import random_lower_string

from app.modules.product.repositories import category_repo
from app.modules.product.schemas.category import CategoryCreate, CategoryUpdate


def test_create_category(db: Session):
    name = random_lower_string()
    desc = random_lower_string()

    category = category_repo.create(db, obj_in=CategoryCreate(
        name=name, description=desc
    ))

    db_obj = category_repo.get(db, id=category.id)

    assert db_obj
    assert db_obj.name == name
    assert db_obj.description == desc


def test_update_category(db: Session):
    name = random_lower_string()
    desc = random_lower_string()

    category = category_repo.create(db, obj_in=CategoryCreate(
        name=name, description=desc
    ))

    new_name = random_lower_string()
    new_desc = random_lower_string()
    new_category = category_repo.update(db, db_obj=category, obj_in=CategoryUpdate(
        name=new_name,
        description=new_desc
    ))

    db_obj = category_repo.get(db, id=category.id)

    assert db_obj.name == new_name
    assert db_obj.description == new_desc


def test_delete_category(db: Session):
    name = random_lower_string()
    desc = random_lower_string()

    category = category_repo.create(db, obj_in=CategoryCreate(
        name=name, description=desc
    ))

    category_repo.remove(db, id=category.id)

    db_obj = category_repo.get(db, id=category.id)

    assert not db_obj
