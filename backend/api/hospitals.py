from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from deps.roles import role_required
import schemas
import models

router = APIRouter(prefix="/hospitals",tags=["Hospitals"])
@router.post("/",dependencies=[Depends(role_required(["superadmin"]))])
def create_hospitals(hospital:schemas.HospitalCreate,db:Session=Depends(get_db)):
    hospital_user = models.User(
        username = hospital.username,
        email = hospital.email,
        password = hospital.password,
        role="hospital"
    )
    db.add(hospital_user)
    db.commit()
    db.refresh(hospital_user)

    new_hospital = models.Hospital(
        name = hospital.name,
        user_id = hospital_user.id
    )
    db.add(new_hospital)
    db.commit()
    db.refresh(new_hospital)

    return {"msg":"Hospital created","hospital_id":new_hospital.id}