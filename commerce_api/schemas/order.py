from pydantic import BaseModel
from datetime import datetime
from .user import UserResponse
from .product import ProductResponse

class OrderCreate(BaseModel):
    quantity: int
    user_id: int
    product_id: int


    
class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int

    class Config:
        from_attributes = True
        
class OrderResponse(BaseModel):
    id: int
    status: str
    items: list[OrderItemResponse]
    user: UserResponse
    

    class Config:
        from_attributes = True

class OrderStatusUpdate(BaseModel):
    status: str