from random import randint
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings


def test_create_auction(
    client: TestClient, superuser_token_headers: dict, db: Session): pass


def test_get_auction(client: TestClient, superuser_token_headers: dict, db: Session): pass
def test_start_auction(
    client: TestClient, superuser_token_headers: dict, db: Session): pass


def test_end_auction(client: TestClient, superuser_token_headers: dict, db: Session): pass
def test_bid_auction(client: TestClient, superuser_token_headers: dict, db: Session): pass
def test_buy_it_now(client: TestClient, superuser_token_headers: dict, db: Session): pass


def test_update_auction(
    client: TestClient, superuser_token_headers: dict, db: Session): pass


def test_delete_auction(
    client: TestClient, superuser_token_headers: dict, db: Session): pass
