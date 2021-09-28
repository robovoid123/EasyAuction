from app.modules.auction.auction.english_auction import EnglishAuction
from app.modules.auction.models.auction_state import AuctionState
from app.tests.utils.utils import random_float
from random import randint
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.core.config import settings
from app.tests.utils.product import create_random_product
from app.tests.utils.auction import create_random_auction
from app.tests.utils.user import create_random_user

from app.modules.auction.repositories import auction_repo


def test_create_auction(
        client: TestClient, superuser_token_headers: dict, db: Session):
    product = create_random_product(db)
    starting_amount = random_float()
    reserve = starting_amount + 2 + random_float()
    bid_cap = reserve + 2 + random_float()
    data = {'auction_in': {
        'starting_amount': starting_amount,
        'reserve': reserve,
        'bid_cap': bid_cap,
        'product_id': product.id
    },
        "ending_date": (datetime.now() + timedelta(days=1)).isoformat()}

    response = client.post(f"{settings.API_PREFIX}/v1/auctions/",
                           headers=superuser_token_headers, json=data)

    print("Response: ", response.json())
    assert response.status_code == 201
    content = response.json()

    assert content["id"]
    assert content["owner_id"]
    assert content["starting_amount"] == starting_amount
    assert content["reserve"] == reserve
    assert content["bid_cap"] == bid_cap
    assert content["product_id"] == product.id


def test_get_auction(client: TestClient, superuser_token_headers: dict, db: Session):
    auction = create_random_auction(db)

    response = client.get(f"{settings.API_PREFIX}/v1/auctions/{auction.id}")

    assert response.status_code == 200
    content = response.json()

    assert content["id"]
    assert content["owner_id"]
    assert content["starting_amount"] == auction.starting_amount
    assert content["reserve"] == auction.reserve
    assert content["bid_cap"] == auction.bid_cap
    assert content["product_id"] == auction.product_id


def test_start_auction(
        client: TestClient, superuser_token_headers: dict, db: Session):
    auction = create_random_auction(db)

    response = client.put(f"{settings.API_PREFIX}/v1/auctions/{auction.id}/start",
                          headers=superuser_token_headers)

    assert response.status_code == 200
    content = response.json()
    db.refresh(auction)
    assert auction.state == AuctionState.ONGOING
    assert content["id"]
    assert content["owner_id"]
    assert content["starting_amount"] == auction.starting_amount
    assert content["reserve"] == auction.reserve
    assert content["bid_cap"] == auction.bid_cap
    assert content["product_id"] == auction.product_id
    assert content["state"] == AuctionState.ONGOING


def test_end_auction(client: TestClient, superuser_token_headers: dict, db: Session):
    auction = create_random_auction(db)
    amount = auction.reserve + random_float()
    bidder = create_random_user(db)
    english = EnglishAuction()
    english.start(db, db_obj=auction)
    english.bid(db, db_obj=auction, amount=amount, bidder_id=bidder.id)

    response = client.put(f"{settings.API_PREFIX}/v1/auctions/{auction.id}/end",
                          headers=superuser_token_headers)

    assert response.status_code == 200
    content = response.json()
    db.refresh(auction)
    assert auction.state == AuctionState.ENDED
    assert content["id"]
    assert content["owner_id"]
    assert content["starting_amount"] == auction.starting_amount
    assert content["reserve"] == auction.reserve
    assert content["bid_cap"] == auction.bid_cap
    assert content["product_id"] == auction.product_id
    assert content["state"] == AuctionState.ENDED


def test_bid_auction(client: TestClient, superuser_token_headers: dict, db: Session):
    auction = create_random_auction(db)
    amount = auction.reserve + random_float()
    english = EnglishAuction()
    english.start(db, db_obj=auction)
    data = amount

    response = client.post(f"{settings.API_PREFIX}/v1/auctions/{auction.id}/bid",
                           headers=superuser_token_headers, json=data)

    assert response.status_code == 200
    content = response.json()
    db.refresh(auction)
    assert auction.winning_bid
    assert auction.last_bid_at


def test_buy_it_now(client: TestClient, superuser_token_headers: dict, db: Session):
    auction = create_random_auction(db)
    english = EnglishAuction()
    english.start(db, db_obj=auction)

    response = client.post(f"{settings.API_PREFIX}/v1/auctions/{auction.id}/buy_it_now",
                           headers=superuser_token_headers)

    assert response.status_code == 200
    content = response.json()
    db.refresh(auction)
    assert auction.final_winner
    assert auction.state == AuctionState.ENDED


def test_update_auction(
    client: TestClient, superuser_token_headers: dict, db: Session): pass


def test_delete_auction(
    client: TestClient, superuser_token_headers: dict, db: Session): pass
