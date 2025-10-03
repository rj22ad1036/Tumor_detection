# dependencies.py

from fastapi import Depends, Request, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
# from models import AdminUser, Employee
from database import SessionLocal
from Utils.jwt_handler import verify_access_token  # your own helper for JWT decoding

# ───────────────────────────────────────────
# OAuth2 scheme (single login endpoint for all roles)
# ───────────────────────────────────────────
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
  # unified login path

# ───────────────────────────────────────────
# Database Dependency
# ───────────────────────────────────────────
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ───────────────────────────────────────────
# Get Current User's Payload from JWT
# ───────────────────────────────────────────
def get_current_user_payload(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        print("📥 Token received:", token)  # Log raw token
        payload = verify_access_token(token)
        print("✅ Token payload:", payload)  # Log decoded payload
        return payload
    except Exception as e:
        print("❌ JWT error:", e)
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# ───────────────────────────────────────────
# Get Current Superadmin
# ───────────────────────────────────────────
# def get_current_superadmin(payload: dict = Depends(get_current_user_payload)):
#     if payload.get("role") != "superadmin":
#         raise HTTPException(status_code=403, detail="Only superadmins can access this route")
#     return payload

# # ───────────────────────────────────────────
# # Get Current Org ID (Organization User)
# # ───────────────────────────────────────────
# def get_current_org_id(payload: dict = Depends(get_current_user_payload)) -> int:
#     if payload.get("role") != "organization":
#         raise HTTPException(status_code=403, detail="Only organization role can access this route")
#     org_id = payload.get("org_id")
#     if not org_id:
#         raise HTTPException(status_code=401, detail="org_id missing from token")
#     return org_id

# # ───────────────────────────────────────────
# # Get Current Admin from Token
# # ───────────────────────────────────────────
# def get_current_admin(
#     payload: dict = Depends(get_current_user_payload),
#     db: Session = Depends(get_db)
# ) -> AdminUser:
#     if payload.get("role") != "admin":
#         raise HTTPException(status_code=403, detail="Only admin access allowed")

#     user_id = payload.get("user_id")  # ✅ This should be in your JWT payload
#     if not user_id:
#         raise HTTPException(status_code=401, detail="Invalid admin token: missing user_id")

#     admin = db.query(AdminUser).filter_by(user_id=user_id).first()
#     if not admin:
#         raise HTTPException(status_code=404, detail="Admin user not found or unauthorized")

#     return admin


# # ───────────────────────────────────────────
# # Get Current Employee from Token
# # ───────────────────────────────────────────
# def get_current_employee(
#     payload: dict = Depends(get_current_user_payload),
#     db: Session = Depends(get_db)
# ) -> Employee:
#     if payload.get("role") != "employee":
#         raise HTTPException(status_code=403, detail="Only employee access allowed")

#     emp_id = payload.get("emp_id")
#     if not emp_id:
#         raise HTTPException(status_code=401, detail="emp_id missing from token")

#     employee = db.query(Employee).filter_by(id=emp_id).first()
#     if not employee:
#         raise HTTPException(status_code=404, detail="Employee not found")

#     return employee
# from typing import Optional
# from fastapi import Query

# def get_org_id_allowing_superadmin(
#     payload: dict = Depends(get_current_user_payload),
#     org_id: Optional[int] = Query(None)
# ) -> int:
#     role = payload.get("role")
#     print(f"🎯 get_org_id_allowing_superadmin: role={role}, org_id={org_id}")
    
#     if role == "organization":
#         return payload.get("org_id")
#     elif role == "superadmin":
#         if org_id is None:
#             raise HTTPException(status_code=400, detail="Superadmin must provide org_id in query")
#         return org_id
#     else:
#         raise HTTPException(status_code=403, detail="Access denied")

