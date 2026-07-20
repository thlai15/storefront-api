from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=2000)
    price_cents: int = Field(gt=0, description="Price in cents, must be positive")
    sku: str = Field(min_length=1, max_length=64)
    stock_quantity: int = Field(ge=0, default=0)


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    price_cents: int | None = Field(default=None, gt=0)
    stock_quantity: int | None = Field(default=None, ge=0)


class ProductOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    description: str
    price_cents: int
    sku: str
    stock_quantity: int
    created_at: datetime
