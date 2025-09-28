from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from schemas import admin
from app import models
from app.database import get_db
from utils.hashing import hash_password, verify_password
from utils.token import create_access_token

router = APIRouter(prefix="/auth", tags=["Admin"])

@router.post("/signup", response_model=admin.AdminModelResponse)
def admin_signup(admin_in: admin.AdminModel, db: Session = Depends(get_db)):
    if db.query(models.Admin).filter(models.Admin.email == admin_in.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    admin_data = admin_in.model_dump()
    admin_data["hashed_password"] = hash_password(admin_data.pop("password"))

    admin = models.Admin(**admin_data)
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin

# @router.post("/login")
# def login(admin_in: admin.AdminLogin, db: Session = Depends(get_db)):
#     admin = db.query(models.Admin).filter(models.Admin.email == admin_in.email).first()
#     if not admin or not verify_password(admin_in.password, admin.hashed_password):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

#     token = create_access_token({"id": admin.id})
#     return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=dict)
def admin_login(admin_in: admin.AdminLogin, db: Session = Depends(get_db)):
    admin = db.query(models.Admin).filter(models.Admin.email == admin_in.email).first()
    if not admin or not verify_password(admin_in.password, admin.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"id": admin.id})
    return {"access_token": token, "token_type": "bearer"}