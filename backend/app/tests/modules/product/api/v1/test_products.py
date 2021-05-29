from random import randint
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.product import random_condition, get_categories
from app.tests.utils.utils import random_lower_string


def test_create_product(
        client: TestClient, superuser_token_headers: dict, db: Session):
    # name = random_lower_string()
    # desc = random_lower_string()
    # condition = random_condition()
    # quantity = randint(1, 100)
    # categories = get_categories(db)
    # categories = [c.name for c in categories]
    # data = {
    #     "name": name,
    #     "description": desc,
    #     "condition": condition,
    #     "quantity": quantity,
    #     "categories": categories
    # }
    # response = client.post(f"{settings.API_PREFIX}/v1/products/", headers=superuser_token_headers,
    #                        json=data)

    # assert response.status_code == 200
    # content = response.json()
    # assert content["name"] == name
    # assert content["description"] == desc
    # assert content["condition"] == condition
    # assert content["quantity"] == quantity
    # assert content["categories"] == categories
    # assert "owner_id" in content
    # assert "id" in content
    pass


def test_get_product(): pass
def test_update_product(): pass
def test_delete_product(): pass
def test_get_reserves(): pass
def test_unreserve(): pass
def test_update_inventory(): pass
def test_add_categories(): pass
def test_delete_categories(): pass
