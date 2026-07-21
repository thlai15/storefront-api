import logging
import uuid

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.db.session import engine
from app.models.base import Base
from app.routers import health, orders, products

from sqlalchemy.orm import Session
from app.models.product import Product

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()

app = FastAPI(
    title="Storefront API",
    version="0.1.0",
    description="Product catalog and order management service for the storefront demo.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(products.router)
app.include_router(orders.router)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    logger.info("storefront-api started, tables ensured")

    with Session(engine) as db:
        if db.query(Product).count() == 0:
            seed_products = [
                Product(id=str(uuid.uuid4()), name="Wireless Mouse", description="Ergonomic wireless mouse", price_cents=2999, sku="SKU-001", stock_quantity=50),
                Product(id=str(uuid.uuid4()), name="Mechanical Keyboard", description="RGB mechanical keyboard", price_cents=8999, sku="SKU-002", stock_quantity=30),
                Product(id=str(uuid.uuid4()), name="USB-C Hub", description="7-in-1 USB-C hub", price_cents=4499, sku="SKU-003", stock_quantity=75),
            ]
            db.add_all(seed_products)
            db.commit()
            logger.info("seeded %d demo products", len(seed_products))
