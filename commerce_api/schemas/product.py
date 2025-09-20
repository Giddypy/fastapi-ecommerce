from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    # description: str | None = None
    price: float
    stock: int

class ProductResponse(ProductCreate):
    id: int

    class Config:
        from_attributes = True
