# core/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    superadmin_email: str
    superadmin_password: str
    jwt_secret_key: str

    class Config:
        env_file = "prod.env"

settings = Settings()
