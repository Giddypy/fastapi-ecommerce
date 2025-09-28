from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models
from schemas import order
from app.database import get_db
from utils.token import get_current_user
from app.models import CartItem, Order, OrderItem




router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/checkout", response_model=order.OrderResponse)
def checkout(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # 1. Get all cart items for the user
    cart_items = db.query(models.CartItem).filter(
        models.CartItem.user_id == current_user.id
    ).all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    # 2. Verify stock for each product
    for item in cart_items:
        if item.product.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for {item.product.name}"
            )

    # 3. Create new order
    new_order = models.Order(user_id=current_user.id, status="pending")
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # 4. Create order items & update stock
    for item in cart_items:
        order_item = models.OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(order_item)
        item.product.stock -= item.quantity

    # 5. Clear the cart
    for item in cart_items:
        db.delete(item)

    db.commit()
    db.refresh(new_order)

    return new_order


# @router.put("/{order_id}/status", response_model=order.OrderResponse)
# def update_order_status(
#     order_id: int,
#     status_update: order.OrderStatusUpdate,
#     db: Session = Depends(get_db),
#     current_user: models.User = Depends(get_current_user)
# ):
#     # only admins can update order status
#     if not current_user.is_admin:
#         raise HTTPException(status_code=403, detail="Not authorized")

#     order = db.query(models.Order).filter(models.Order.id == order_id).first()
#     if not order:
#         raise HTTPException(status_code=404, detail="Order not found")

#     valid_statuses = ["pending", "processing", "shipped", "delivered", "cancelled"]
#     if status_update.status not in valid_statuses:
#         raise HTTPException(
#             status_code=400,
#             detail=f"Invalid status. Must be one of: {valid_statuses}"
#         )

#     order.status = status_update.status
#     db.commit()
#     db.refresh(order)

#     return order



# @router.get("/my-orders", response_model=list[order.OrderResponse])
# def get_my_orders(
#     db: Session = Depends(get_db),
#     current_user: models.User = Depends(get_current_user)
# ):
#     orders = (
#         db.query(models.Order)
#         .filter(models.Order.user_id == current_user.id)
#         .all()
#     )
#     return orders


# @router.get("/", response_model=list[order.OrderResponse])
# def get_all_orders(
#     db: Session = Depends(get_db),
#     current_user: models.User = Depends(get_current_user)
# ):
#     if not current_user.is_admin:
#         raise HTTPException(status_code=403, detail="Not authorized")

#     orders = db.query(models.Order).all()
#     return orders


# @router.get("/{order_id}", response_model=order.OrderResponse)
# def get_order(
#     order_id: int,
#     db: Session = Depends(get_db),
#     current_user: models.User = Depends(get_current_user)
# ):
#     order = db.query(models.Order).filter(models.Order.id == order_id).first()
#     if not order:
#         raise HTTPException(status_code=404, detail="Order not found")

#     if not current_user.is_admin and order.user_id != current_user.id:
#         raise HTTPException(status_code=403, detail="Not authorized")

#     return order


