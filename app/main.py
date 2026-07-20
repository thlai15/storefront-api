import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.db.session import engine
from app.models.base import Base
from app.routers import health, orders, products

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
    # Demo-only: create tables at startup. In a real deployment this would
    # be handled by a migration tool (e.g. Alembic) run as a separate step.
    Base.metadata.create_all(bind=engine)
    logger.info("storefront-api started, tables ensured")
