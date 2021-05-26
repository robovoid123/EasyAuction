from random import randint
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.product import random_condition, get_categories
from app.tests.utils.utils import random_lower_string, random_float


def test_create_product(
        client: TestClient, superuser_token_headers: dict, db: Session):
    name = random_lower_string()
    desc = random_lower_string()
    condition = random_condition()
    quantity = randint(1, 100)
    categories = get_categories(db)
    categories = [c.name for c in categories]
    data = {
        "name": name,
        "description": desc,
        "condition": condition,
        "quantity": quantity,
        "categories": categories
    }
    response = client.post(f"{settings.API_V1_STR}/products/", headers=superuser_token_headers,
                           json=data)

    assert response.status_code == 200
    content = response.json()
    assert content["name"] == name
    assert content["description"] == desc
    assert content["condition"] == condition
    assert "inventory" in content
    assert "id" in content["inventory"]
    assert content["inventory"]["quantity"] == quantity
    assert "categories" in content
    assert "owner_id" in content
    assert "id" in content


def test_get_product(): pass
def test_update_product(): pass
