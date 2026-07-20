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


def test_create_and_get_product():
    resp = client.post(
        "/products",
        json={"name": "T-Shirt", "sku": "TS-001", "price_cents": 1999, "stock_quantity": 10},
    )
    assert resp.status_code == 201
    product = resp.json()
    assert product["sku"] == "TS-001"

    get_resp = client.get(f"/products/{product['id']}")
    assert get_resp.status_code == 200
    assert get_resp.json()["name"] == "T-Shirt"


def test_duplicate_sku_rejected():
    client.post("/products", json={"name": "A", "sku": "DUP", "price_cents": 100, "stock_quantity": 1})
    resp = client.post("/products", json={"name": "B", "sku": "DUP", "price_cents": 200, "stock_quantity": 1})
    assert resp.status_code == 409


def test_get_missing_product_returns_404():
    resp = client.get("/products/does-not-exist")
    assert resp.status_code == 404


def test_invalid_price_rejected():
    resp = client.post("/products", json={"name": "Bad", "sku": "BAD-1", "price_cents": -5, "stock_quantity": 1})
    assert resp.status_code == 422
