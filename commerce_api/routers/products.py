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
