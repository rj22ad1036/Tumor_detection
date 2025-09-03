# schemas/auth.py
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str  # "superadmin", "hospital", "doctor", "patient"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
class HospitalCreate(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str