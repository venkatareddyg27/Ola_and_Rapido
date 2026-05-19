from passlib.context import CryptContext
from jose import jwt
import re
from datetime import datetime, timedelta
from app.core.config import Settings

settings = Settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password
def hash_password(text: str):
    return pwd_context.hash(text)

# Verify password
def verify_password(text: str, hash: str):
    return pwd_context.verify(text, hash)

# Access token creation

ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# Refresh token
def create_refresh_token(user_id: int):
    payload = {"user_id": user_id, "exp": datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# Decode token
def decode_access_token(token: str):
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except Exception:
        return None
# app/core/security.py

def decode_refresh_token(token: str):
    return decode_access_token(token)


