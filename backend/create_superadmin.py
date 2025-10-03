# create_superadmin.py
from sqlalchemy.orm import Session
from database import SessionLocal
import models
from Utils.security import hash_password
from Utils.config import settings


def create_superadmin():
    db: Session = SessionLocal()

    # Check if superadmin exists
    existing_user = db.query(models.User).filter_by(username="superadmin").first()
    if existing_user:
        print("✅ Superadmin already exists:", existing_user.email)
        return

    # Create new superadmin
    superadmin = models.User(
        username="superadmin",
        email=settings.superadmin_email,
        password=hash_password(settings.superadmin_password),
        photo="default.jpg",
        role="superadmin",   # must match your roles ("superadmin", "hospital", "doctor", "patient")
        is_active=True,
    )

    db.add(superadmin)
    db.commit()
    db.refresh(superadmin)
    print("🎉 Superadmin created with ID:", superadmin.id)


if __name__ == "__main__":
    create_superadmin()
