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


@router.get("/",dependencies=[Depends(role_required(["superadmin"]))])
def list_hospitals(db:Session=Depends(get_db)):
    hospitals = db.query(models.hospital).all()
    return hospitals

@router.get("/hos/{hospital_id}",dependencies=[Depends(role_required(["superadmin"]))])
def get_hospital(hospital_id:int,db:Session=Depends(get_db)):
    hospital = db.query(models.Hospital).filter(models.Hospital.id==hospital_id).first()
    if not hospital:
        raise HTTPException(status_code=404,detail="Hospital not found")
    return hospital

@router.put("update/{hospital_id}",dependencies=[Depends(role_required(["superadmin"]))])
def update_hospital(hospital_id:int,updated:schemas.HospitalUpdate,db:Session = Depends(get_db)):
    hospital = db.query(models.Hospital).filter(models.Hospital.id == hospital_id).first()
    if not hospital:
        raise HTTPException(status_code=404,detail="Hospital not found")
    if updated.username or updated.email or updated.password:
        user = db.query(models.User).filter(models.User.id==hospital_id).first()
        if updated.username:
            user.username = updated.username
        if updated.email:
            user.email = updated.email
        if updated.password:
            user.password = updated.password
        db.add(user)
    db.add(hospital)
    db.commit()
    db.refresh(hospital)
    return {"msg":"Hospital Updated","hospital_id":hospital.id}

@router.delete("/del/{hospital_id}",dependencies=[Depends(role_required(["superadmin"]))])
def delete_hospital(hospital_id:int,db:Session=Depends(get_db)):
    hospital = db.query(models.Hospital).filter(models.Hospital.id==hospital_id).first()
    if not hospital:
        raise HTTPException(status_code=404,detail="Hospital not Found")
    user = db.query(models.User).filter(models.User.id == hospital.user_id).first()
    if user:
        db.delete(user)
    db.delete(hospital)
    db.commit()
    return {"msg":"Hospital deleted"}