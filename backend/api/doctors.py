from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from deps.roles import role_required
import schemas
import models

router = APIRouter(prefix="/doctors", tags=["Doctors"])


# ✅ CREATE Doctor
@router.post("/", dependencies=[Depends(role_required(["superadmin", "hospital"]))])
def create_doctor(doctor: schemas.DoctorCreate, db: Session = Depends(get_db)):
    # Ensure hospital exists
    hospital = db.query(models.Hospital).filter(models.Hospital.id == doctor.hospital_id).first()
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")

    # Create User entry
    doctor_user = models.User(
        username=doctor.username,
        email=doctor.email,
        password=doctor.password,  # ⚠️ hash before storing in real code!
        role="doctor"
    )
    db.add(doctor_user)
    db.commit()
    db.refresh(doctor_user)

    # Create Doctor entry
    new_doctor = models.Doctor(
        first_name=doctor.first_name,
        last_name=doctor.last_name,
        specialization=doctor.specialization,
        user_id=doctor_user.id,
        hospital_id=doctor.hospital_id
    )
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)

    return {"msg": "Doctor created", "doctor_id": new_doctor.id}


# ✅ READ (list all doctors)
@router.get("/", dependencies=[Depends(role_required(["superadmin", "hospital"]))])
def list_doctors(db: Session = Depends(get_db)):
    doctors = db.query(models.Doctor).all()
    return doctors


# ✅ READ (get single doctor)
@router.get("/{doctor_id}", dependencies=[Depends(role_required(["superadmin", "hospital"]))])
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


# ✅ UPDATE Doctor
@router.put("/{doctor_id}", dependencies=[Depends(role_required(["superadmin", "hospital"]))])
def update_doctor(doctor_id: int, updated: schemas.DoctorUpdate, db: Session = Depends(get_db)):
    doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    # Update doctor details
    doctor.first_name = updated.first_name or doctor.first_name
    doctor.last_name = updated.last_name or doctor.last_name
    doctor.specialization = updated.specialization or doctor.specialization
    if updated.hospital_id:
        hospital = db.query(models.Hospital).filter(models.Hospital.id == updated.hospital_id).first()
        if not hospital:
            raise HTTPException(status_code=404, detail="Hospital not found")
        doctor.hospital_id = updated.hospital_id

    # Update user info
    user = db.query(models.User).filter(models.User.id == doctor.user_id).first()
    if updated.username:
        user.username = updated.username
    if updated.email:
        user.email = updated.email
    if updated.password:
        user.password = updated.password  # ⚠️ hash before storing in real code!

    db.add(doctor)
    db.add(user)
    db.commit()
    db.refresh(doctor)

    return {"msg": "Doctor updated", "doctor_id": doctor.id}


# ✅ DELETE Doctor
@router.delete("/{doctor_id}", dependencies=[Depends(role_required(["superadmin", "hospital"]))])
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    # Delete user as well
    user = db.query(models.User).filter(models.User.id == doctor.user_id).first()
    if user:
        db.delete(user)

    db.delete(doctor)
    db.commit()
    return {"msg": "Doctor deleted"}
