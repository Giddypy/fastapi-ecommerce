from pydantic import BaseModel

class ShippingCreate(BaseModel):
    address: str
    city: str
    postal_code: str
    country: str

class ShippingResponse(ShippingCreate):
    id: int
    order_id: int

    class Config:
        from_attributes = True
