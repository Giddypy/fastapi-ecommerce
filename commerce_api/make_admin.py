# make_admin.py
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models

def make_admin(email: str):
    db: Session = SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.email == email).first()
        if not user:
            print("❌ User not found")
            return
        user.is_admin = True
        db.commit()
        print(f"✅ {user.email} is now an admin")
    finally:
        db.close()


if __name__ == "__main__":
    # 👇 change this email to the user you want to promote
    make_admin("pee@gmail.com")
