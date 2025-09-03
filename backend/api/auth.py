# routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from Utils.security import verify_password, hash_password
from Utils.jwt_handler import create_access_token
from schemas import UserLogin, Token
from models import User
from Utils.config import settings

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    # 🔑 1. Check if superadmin (from .env)
    if user.email == settings.superadmin_email and user.password == settings.superadmin_password:
        token = create_access_token({"sub": "0", "role": "superadmin"})  # sub=0 → not in DB
        return {"access_token": token, "token_type": "bearer"}

    # 🔑 2. Otherwise check normal users from DB
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(db_user.id), "role": db_user.role})
    return {"access_token": token, "token_type": "bearer"}
