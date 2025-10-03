from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    superadmin_email: str
    superadmin_password: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = "prod.env"


settings = Settings()
