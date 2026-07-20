import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.db.session import get_db
from app.models.order import Order, OrderItem, OrderStatus
from app.models.product import Product
from app.schemas.order import OrderCreate, OrderOut

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)) -> Order:
    order = Order(id=str(uuid.uuid4()), customer_email=payload.customer_email, status=OrderStatus.PENDING.value)

    for item in payload.items:
        product = db.get(Product, item.product_id)
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"product '{item.product_id}' not found",
            )
        if product.stock_quantity < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"insufficient stock for product '{product.id}': "
                f"requested {item.quantity}, available {product.stock_quantity}",
            )
        product.stock_quantity -= item.quantity
        order.items.append(
            OrderItem(
                id=str(uuid.uuid4()),
                product_id=product.id,
                quantity=item.quantity,
                unit_price_cents=int(product.price_cents),
            )
        )

    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@router.get("", response_model=list[OrderOut])
def list_orders(
    skip: int = 0, limit: int = 50, db: Session = Depends(get_db)
) -> list[Order]:
    limit = min(limit, 200)
    return (
        db.query(Order)
        .options(joinedload(Order.items))
        .offset(skip)
        .limit(limit)
        .unique()
        .all()
    )


@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: str, db: Session = Depends(get_db)) -> Order:
    order = (
        db.query(Order)
        .options(joinedload(Order.items))
        .filter(Order.id == order_id)
        .first()
    )
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order not found")
    return order
