from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from pydantic_settings import BaseSettings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Settings(BaseSettings):
    SECRET_KEY: str = "change-me"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"
    class Config:
        env_file = ".env"

settings = Settings()

def get_password_hash(p: str) -> str:
    return pwd_context.hash(p)

def verify_password(p: str, hp: str) -> bool:
    return pwd_context.verify(p, hp)

def create_access_token(data: dict, expires_minutes: int | None = None) -> str:
    to_encode = data.copy()
    exp = datetime.now(timezone.utc) + timedelta(
        minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": exp})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
