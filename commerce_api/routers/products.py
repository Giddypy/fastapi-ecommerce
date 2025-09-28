from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models
from schemas import product
from app.database import get_db
from utils.dependencies import admin_required



router = APIRouter(prefix="/products", tags=["Products"])



@router.post("/", response_model=product.ProductResponse)
def create_product(product_in: product.ProductCreate,
                   db: Session = Depends(get_db),
                   current_user: models.User = Depends(admin_required)
                   
                   ):
    

    product = models.Product(**product_in.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product



@router.get("/", response_model=list[product.ProductResponse])
def list_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()


@router.delete("/{product_id}", response_model=product.ProductResponse)
def delete_product(product_id: int,
                   db: Session = Depends(get_db),
                   current_user: models.User = Depends(admin_required)
                   ):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    
    if not product:
        raise HTTPException(status_code=403, detail= "Product not found")
    db.delete(product)
    db.commit()
    return {"detail": f"product {product_id} deleted successfully"}