from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from deps.roles import role_required
import schemas
import models

router = APIRouter(prefix="/hospitals", tags=["Hospitals"])


# ✅ Create Hospital
@router.post("/", dependencies=[Depends(role_required(["superadmin"]))])
def create_hospital(hospital: schemas.HospitalCreate, db: Session = Depends(get_db)):
    # Create user with hospital role
    hospital_user = models.User(
        username=hospital.username,
        email=hospital.email,
        password=hospital.password,  # TODO: hash password before saving
        role="hospital",
    )
    db.add(hospital_user)
    db.commit()
    db.refresh(hospital_user)

    # Create hospital linked to user
    new_hospital = models.Hospital(
        name=hospital.name,
        user_id=hospital_user.id,
    )
    db.add(new_hospital)
    db.commit()
    db.refresh(new_hospital)

    return {"msg": "Hospital created", "hospital_id": new_hospital.id}


# ✅ List Hospitals
@router.get("/g", dependencies=[Depends(role_required(["superadmin"]))])
def list_hospitals(db: Session = Depends(get_db)):
    hospitals = db.query(models.Hospital).all()
    return hospitals


# ✅ Get single hospital
@router.get("/{hospital_id}", dependencies=[Depends(role_required(["superadmin"]))])
def get_hospital(hospital_id: int, db: Session = Depends(get_db)):
    hospital = db.query(models.Hospital).filter(models.Hospital.id == hospital_id).first()
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return hospital


# ✅ Update hospital
@router.put("/{hospital_id}", dependencies=[Depends(role_required(["superadmin"]))])
def update_hospital(hospital_id: int, updated: schemas.HospitalUpdate, db: Session = Depends(get_db)):
    hospital = db.query(models.Hospital).filter(models.Hospital.id == hospital_id).first()
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")

    # Update hospital name if provided
    if updated.name:
        hospital.name = updated.name

    # Update linked user if fields provided
    user = db.query(models.User).filter(models.User.id == hospital.user_id).first()
    if updated.username:
        user.username = updated.username
    if updated.email:
        user.email = updated.email
    if updated.password:
        user.password = updated.password  # TODO: hash password

    db.commit()
    db.refresh(hospital)

    return {"msg": "Hospital updated", "hospital_id": hospital.id}


# ✅ Delete hospital
@router.delete("/{hospital_id}", dependencies=[Depends(role_required(["superadmin"]))])
def delete_hospital(hospital_id: int, db: Session = Depends(get_db)):
    hospital = db.query(models.Hospital).filter(models.Hospital.id == hospital_id).first()
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")

    # Delete linked user
    user = db.query(models.User).filter(models.User.id == hospital.user_id).first()
    if user:
        db.delete(user)

    db.delete(hospital)
    db.commit()

    return {"msg": "Hospital deleted"}
