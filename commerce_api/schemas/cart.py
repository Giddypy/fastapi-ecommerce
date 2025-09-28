
from pydantic import BaseModel

class CartItemBase(BaseModel):
    product_id: int
    # product_name: str
    quantity: int = 1

class CartItemCreate(CartItemBase):
    pass

class CartItemResponse(CartItemBase):
    id: int
    user_id: int


    class Config:
        from_attributes = True
