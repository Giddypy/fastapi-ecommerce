from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi import Security
from fastapi.security import OAuth2PasswordRequestForm, HTTPBearer
from schemas import user
from app import models
from app.database import get_db
from utils.hashing import hash_password, verify_password
from utils.token import create_access_token, create_refresh_token, verify_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", response_model=user.UserResponse)
def signup(user_in: user.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == user_in.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    user_data = user_in.model_dump()
    user_data["hashed_password"] = hash_password(user_data.pop("password"))

    user = models.User(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# @router.post("/login")
# def login(user_in: user.UserLogin, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.email == user_in.email).first()
#     if not user or not verify_password(user_in.password, user.hashed_password):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

#     access_token = create_access_token({"id": user.id})
#     refresh_token = create_refresh_token({"sub": str(user.id)})


#     return {
#         "access_token": access_token,
#         "refresh_token": refresh_token,
#         "token_type": "bearer"
#     }


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }




refresh_oauth2_scheme = HTTPBearer()
@router.post("/refresh")
def refresh_token(refresh_token: str = Security(refresh_oauth2_scheme), db: Session = Depends(get_db)):
    user = verify_token(refresh_token, db, token_type="refresh")
    new_access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": new_access_token, "token_type": "bearer"}