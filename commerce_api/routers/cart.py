# app/routers/cart.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models
from schemas import cart
from app.database import get_db
from utils.token import get_current_user

router = APIRouter(prefix="/cart", tags=["Cart"])

# @router.post("/", response_model=cart.CartItemResponse)
# def add_to_cart(
#     item: cart.CartItemCreate,
#     db: Session = Depends(get_db),
#     current_user: models.User = Depends(get_current_user)  # <-- secured with access token
# ):
#     product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
#     if not product:
#         raise HTTPException(status_code=404, detail="Product not found")

#     cart_item = db.query(models.CartItem).filter(
#         models.CartItem.user_id == current_user.id,
#         models.CartItem.product_id == item.product_id
#     ).first()

#     if cart_item:
#         cart_item.quantity += item.quantity
#     else:
#         cart_item = models.CartItem(user_id=current_user.id, **item.model_dump())
#         db.add(cart_item)

#     db.commit()
#     db.refresh(cart_item)
#     return cart_item
@router.post("/", status_code=status.HTTP_201_CREATED)
def add_to_cart(
    item: cart.CartItemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Check if product exists
    product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Check if cart item already exists
    cart_item = db.query(models.CartItem).filter(
        models.CartItem.user_id == current_user.id,
        models.CartItem.product_id == item.product_id
    ).first()

    if cart_item:
        cart_item.quantity += item.quantity
    else:
        cart_item = models.CartItem(
            user_id=current_user.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
    
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return {"message": "Item added to cart", "cart_item": cart_item}


@router.get("/", response_model=list[cart.CartItemResponse])
def get_cart(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.CartItem).filter(models.CartItem.user_id == current_user.id).all()


@router.put("/{id}", response_model=cart.CartItemResponse)
def update_cart_item(
    id: int,
    item: cart.CartItemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    cart_item = db.query(models.CartItem).filter(
        models.CartItem.id == id, models.CartItem.user_id == current_user.id
    ).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    cart_item.quantity = item.quantity
    db.commit()
    db.refresh(cart_item)
    return cart_item


@router.delete("/{id}", status_code=204)
def remove_cart_item(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    cart_item = db.query(models.CartItem).filter(
        models.CartItem.id == id, models.CartItem.user_id == current_user.id
    ).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(cart_item)
    db.commit()
    return
