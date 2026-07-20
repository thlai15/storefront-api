import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.session import get_db
from app.main import app
from app.models.base import Base

engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def _setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def _create_product(stock=5):
    resp = client.post(
        "/products",
        json={"name": "Mug", "sku": f"MUG-{stock}", "price_cents": 1200, "stock_quantity": stock},
    )
    return resp.json()


def test_create_order_decrements_stock():
    product = _create_product(stock=5)
    resp = client.post(
        "/orders",
        json={"customer_email": "a@example.com", "items": [{"product_id": product["id"], "quantity": 2}]},
    )
    assert resp.status_code == 201
    order = resp.json()
    assert order["items"][0]["quantity"] == 2

    product_resp = client.get(f"/products/{product['id']}")
    assert product_resp.json()["stock_quantity"] == 3


def test_order_rejected_when_insufficient_stock():
    product = _create_product(stock=1)
    resp = client.post(
        "/orders",
        json={"customer_email": "a@example.com", "items": [{"product_id": product["id"], "quantity": 5}]},
    )
    assert resp.status_code == 409


def test_order_rejected_for_unknown_product():
    resp = client.post(
        "/orders",
        json={"customer_email": "a@example.com", "items": [{"product_id": "unknown", "quantity": 1}]},
    )
    assert resp.status_code == 404
