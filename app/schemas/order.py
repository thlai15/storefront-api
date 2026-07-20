from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.order import OrderStatus


class OrderItemCreate(BaseModel):
    product_id: str
    quantity: int = Field(gt=0)


class OrderCreate(BaseModel):
    customer_email: EmailStr
    items: list[OrderItemCreate] = Field(min_length=1)


class OrderItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: str
    quantity: int
    unit_price_cents: int


class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    customer_email: str
    status: OrderStatus
    created_at: datetime
    items: list[OrderItemOut]
