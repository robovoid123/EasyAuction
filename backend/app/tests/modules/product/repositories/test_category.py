from sqlalchemy.orm import Session

from app.tests.utils.utils import random_lower_string

from app.modules.product.repositories import category_repo


def test_get_categories_with_name(db: Session):
    cat1 = random_lower_string()
    cat2 = random_lower_string()
    cat3 = random_lower_string()

    cat_db1 = category_repo.create(db, obj_in={"name": cat1})
    cat_db2 = category_repo.create(db, obj_in={"name": cat2})
    cat_db3 = category_repo.create(db, obj_in={"name": cat3})

    cat_list = category_repo.get_with_names(db, [cat1, cat2, cat3])

    assert cat_list
    assert cat_list == [cat_db1, cat_db2, cat_db3]
    name_list = [c.name for c in cat_list]
    assert name_list == [cat1, cat2, cat3]


def test_get_multi_with_ids(db: Session):
    cat1 = random_lower_string()
    cat2 = random_lower_string()
    cat3 = random_lower_string()

    cat_db1 = category_repo.create(db, obj_in={"name": cat1})
    cat_db2 = category_repo.create(db, obj_in={"name": cat2})
    cat_db3 = category_repo.create(db, obj_in={"name": cat3})

    cat_list = category_repo.get_multi_with_ids(
        db, ids=[cat_db1.id, cat_db2.id, cat_db3.id])

    assert cat_list == [cat_db1, cat_db2, cat_db3]
