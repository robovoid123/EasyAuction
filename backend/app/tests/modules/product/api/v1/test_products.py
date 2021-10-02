from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.core.config import settings

from app.tests.utils.utils import random_lower_string
from app.tests.utils.product import create_random_category, create_random_product

from app.modules.product.repositories import product_repo
from app.modules.product.schemas.product import ProductCreate


def test_create_product(client: TestClient, superuser_token_headers: dict, db: Session):
    name = random_lower_string()
    desc = random_lower_string()
    cat1 = create_random_category(db)
    data = {"product_in": {"name": name, "description": desc},
            "categories": [cat1.name, cat1.name]}

    response = client.post(f"{settings.API_PREFIX}/v1/products/",
                           headers=superuser_token_headers, json=data)

    assert response.status_code == 201
    content = response.json()

    assert content["name"] == name
    assert content["description"] == desc
    assert content["owner_id"]


def test_get_product(client: TestClient, db: Session):
    name = random_lower_string()
    desc = random_lower_string()

    product = product_repo.create(db, obj_in=ProductCreate(
        name=name, description=desc
    ))

    data = {"name": name, "description": desc}

    response = client.get(f"{settings.API_PREFIX}/v1/products/{product.id}")

    assert response.status_code == 200
    content = response.json()

    assert content["name"] == name
    assert content["description"] == desc


def test_update_product(client: TestClient, superuser_token_headers: dict, db: Session):
    name = random_lower_string()
    desc = random_lower_string()

    product = product_repo.create(db, obj_in=ProductCreate(
        name=name, description=desc
    ))

    new_name = random_lower_string()
    new_desc = random_lower_string()
    data = {"name": new_name, "description": new_desc}

    response = client.put(f"{settings.API_PREFIX}/v1/products/{product.id}",
                          headers=superuser_token_headers, json=data)

    assert response.status_code == 200
    content = response.json()

    assert content["name"] == new_name
    assert content["description"] == new_desc


def test_delete_product(client: TestClient, superuser_token_headers: dict, db: Session):

    name = random_lower_string()
    desc = random_lower_string()

    product = product_repo.create(db, obj_in=ProductCreate(
        name=name, description=desc
    ))

    response = client.delete(f"{settings.API_PREFIX}/v1/products/{product.id}",
                             headers=superuser_token_headers)

    assert response.status_code == 200
    content = response.json()

    assert content["name"] == name
    assert content["description"] == desc


def test_add_category(client: TestClient, superuser_token_headers: dict, db: Session):
    product = create_random_product(db)
    cat1 = create_random_category(db)

    data = cat1.id

    response = client.post(f"{settings.API_PREFIX}/v1/products/{product.id}/categories",
                           headers=superuser_token_headers, json=data)

    assert response.status_code == 200
    content = response.json()
    db.refresh(product)
    assert cat1 in product.categories


def test_remove_categories(client: TestClient, superuser_token_headers: dict, db: Session):
    product = create_random_product(db)
    cat1 = create_random_category(db)

    product_repo.add_category(db, db_obj=product, category=cat1)
    db.refresh(product)
    assert cat1 in product.categories

    response = client.delete(f"{settings.API_PREFIX}/v1/products/{product.id}/categories/{cat1.id}",
                             headers=superuser_token_headers)

    assert response.status_code == 200
    content = response.json()
    db.refresh(product)
    assert cat1 not in product.categories


def test_get_user_products(client: TestClient, superuser_token_headers: dict, db: Session):
    assert False
