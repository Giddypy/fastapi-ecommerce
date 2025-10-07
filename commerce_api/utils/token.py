# app/utils/token.py
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models
from app.database import get_db
from utils.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS

security = HTTPBearer()

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "scope": "access_token"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


    
def create_refresh_token(data: dict):
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = data.copy()
    to_encode.update({"exp": expire, "scope": "refresh_token"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



def verify_token(token: str, db: Session, token_type: str = "access"):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # ✅ Check scope
        if token_type == "access" and payload.get("scope") != "access_token":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token"
            )
        if token_type == "refresh" and payload.get("scope") != "refresh_token":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        # ✅ Use "sub" instead of "id"
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing user id"
            )

        # ✅ Fetch user from DB
        user = db.query(models.User).filter(models.User.id == int(user_id)).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        return user

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate token"
        )


# 🔹 Dependency to get current logged-in user
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials  # ✅ raw token string
    return verify_token(token, db, token_type="access")