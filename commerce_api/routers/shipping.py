from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from  schemas import shipping
from app import models
from app.database import get_db
from utils.token import get_current_user

router = APIRouter(prefix="/shipping", tags=["Shipping"])

@router.post("/{order_id}", response_model=shipping.ShippingResponse)
def add_shipping(
    order_id: int,
    shipping_data: shipping.ShippingCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to add shipping to this order")

    if order.shipping:
        raise HTTPException(status_code=400, detail="Shipping details already exist for this order")

    shipping = models.Shipping(order_id=order_id, **shipping_data.model_dump())
    db.add(shipping)
    db.commit()
    db.refresh(shipping)

    return shipping



@router.get("/{order_id}", response_model=shipping.ShippingResponse)
def get_shipping(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    shipping = db.query(models.Shipping).filter(models.Shipping.order_id == order_id).first()

    if not shipping:
        raise HTTPException(status_code=404, detail="Shipping details not found")

    order = db.query(models.Order).filter(models.Order.id == order_id).first()

    if order.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to view this shipping details")

    return shipping
