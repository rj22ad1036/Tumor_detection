from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from datetime import datetime
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    phone = Column(String(15), nullable=True)
    address = Column(String(255), nullable=True)
    photo = Column(String, nullable=True, default="default.jpg")
    role = Column(String(20), nullable=False)  # "superadmin", "hospital", "doctor", "patient"
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    hospital = relationship("Hospital", back_populates="user", uselist=False)
    doctor = relationship("Doctor", back_populates="user", uselist=False)
    patient = relationship("Patient", back_populates="user", uselist=False)


class Hospital(Base):
    __tablename__ = "hospitals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="hospital")
    doctors = relationship("Doctor", back_populates="hospital", cascade="all, delete-orphan")
    timeslots = relationship("TimeSlot", back_populates="hospital", cascade="all, delete-orphan")


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    specialization = Column(String(100))
    user_id = Column(Integer, ForeignKey("users.id"))
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))

    user = relationship("User", back_populates="doctor")
    hospital = relationship("Hospital", back_populates="doctors")
    patients = relationship("Patient", back_populates="doctor", cascade="all, delete-orphan")
    timeslots = relationship("TimeSlot", back_populates="doctor", cascade="all, delete-orphan")  # FIXED missing


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)  # FIXED typo
    last_name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)
    medical_record = Column(String(255))
    user_id = Column(Integer, ForeignKey("users.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))

    user = relationship("User", back_populates="patient")
    doctor = relationship("Doctor", back_populates="patients")

    reports = relationship("PatientReport", back_populates="patient", cascade="all, delete-orphan")
    scans = relationship("PatientScan", back_populates="patient", cascade="all, delete-orphan")
    plans = relationship("PatientPlan", back_populates="patient", cascade="all, delete-orphan")


class TimeSlot(Base):
    __tablename__ = "timeslots"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    is_booked = Column(Boolean, default=False)

    doctor = relationship("Doctor", back_populates="timeslots")
    hospital = relationship("Hospital", back_populates="timeslots")


class PatientReport(Base):
    __tablename__ = "patient_reports"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    file_path = Column(String, nullable=False)
    analyzed_data = Column(String)

    patient = relationship("Patient", back_populates="reports")


class PatientScan(Base):
    __tablename__ = "patient_scans"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    image_path = Column(String, nullable=False)
    result = Column(String)

    patient = relationship("Patient", back_populates="scans")


class PatientPlan(Base):
    __tablename__ = "patient_plans"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    disease = Column(String, nullable=False)
    recovery_period_days = Column(Integer)
    medicines = Column(String)
    diet_plan = Column(String)
    exercise_plan = Column(String)
    next_checkup = Column(DateTime)

    patient = relationship("Patient", back_populates="plans")
