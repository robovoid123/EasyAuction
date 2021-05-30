from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings

from app.tests.utils.utils import random_lower_string

from app.modules.product.repositories import category_repo
from app.modules.product.schemas.category import CategoryCreate


def test_create_category(client: TestClient, superuser_token_headers: dict, db: Session):
    name = random_lower_string()
    desc = random_lower_string()
    data = {"name": name, "description": desc}

    response = client.post(f"{settings.API_PREFIX}/v1/categories/",
                           headers=superuser_token_headers, json=data)

    assert response.status_code == 201
    content = response.json()

    assert content["name"] == name
    assert content["description"] == desc


def test_get_category(client: TestClient, db: Session):
    name = random_lower_string()
    desc = random_lower_string()

    category = category_repo.create(db, obj_in=CategoryCreate(
        name=name, description=desc
    ))

    data = {"name": name, "description": desc}

    response = client.get(f"{settings.API_PREFIX}/v1/categories/{category.id}")

    assert response.status_code == 200
    content = response.json()

    assert content["name"] == name
    assert content["description"] == desc


def test_update_category(client: TestClient, superuser_token_headers: dict, db: Session):
    name = random_lower_string()
    desc = random_lower_string()

    category = category_repo.create(db, obj_in=CategoryCreate(
        name=name, description=desc
    ))

    new_name = random_lower_string()
    new_desc = random_lower_string()
    data = {"name": new_name, "description": new_desc}

    response = client.put(f"{settings.API_PREFIX}/v1/categories/{category.id}",
                          headers=superuser_token_headers, json=data)

    assert response.status_code == 200
    content = response.json()

    assert content["name"] == new_name
    assert content["description"] == new_desc


def test_delete_category(client: TestClient, superuser_token_headers: dict, db: Session):

    name = random_lower_string()
    desc = random_lower_string()

    category = category_repo.create(db, obj_in=CategoryCreate(
        name=name, description=desc
    ))

    response = client.delete(f"{settings.API_PREFIX}/v1/categories/{category.id}",
                             headers=superuser_token_headers)

    assert response.status_code == 200
    content = response.json()

    assert content["name"] == name
    assert content["description"] == desc
