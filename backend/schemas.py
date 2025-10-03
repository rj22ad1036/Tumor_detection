# schemas/auth.py
from pydantic import BaseModel, EmailStr
from typing import Optional
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
    token_type: str
    role: str

class HospitalCreate(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str

class HospitalUpdate(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] =None
    password:Optional[str] =None


class DoctorCreate(BaseModel):
    first_name:str
    last_name:str
    specialization:Optional[str]=None
    username:str
    email:str
    password:str
    hospital_id:int


class DoctorUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    specialization: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    hospital_id: Optional[int] = None
