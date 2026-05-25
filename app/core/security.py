import re
from datetime import (datetime,timedelta,timezone)
from typing import Optional
from jose import (jwt,JWTError)
from passlib.context import CryptContext
from fastapi import (Depends,HTTPException,status)
from fastapi.security import (HTTPBearer,HTTPAuthorizationCredentials)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.core.database import get_db
from app.models.user_models import User
from app.core.enums import UserRole



pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
security = HTTPBearer()
optional_security = HTTPBearer(auto_error=False)

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = (settings.ACCESS_TOKEN_EXPIRE_MINUTES)
REFRESH_TOKEN_EXPIRE_DAYS = (settings.REFRESH_TOKEN_EXPIRE_DAYS)
BLACKLISTED_TOKENS = set()

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str,hashed_password: str) -> bool:
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(user_id: str,expires_delta: Optional[timedelta] = None):

    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    payload = {
        "sub": str(user_id),
        "type": "access",
        "exp": expire
    }

    encoded_jwt = jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt



def create_refresh_token(user_id: str,expires_delta: Optional[timedelta] = None):

    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(
            days=REFRESH_TOKEN_EXPIRE_DAYS))

    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "exp": expire
    }

    encoded_jwt = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt

def verify_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM])

        return payload

    except JWTError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token")

def decode_access_token(token: str):

    return verify_token(token)


def decode_refresh_token(token: str):

    return verify_token(token)


async def get_current_user(credentials:
    HTTPAuthorizationCredentials = Depends(
        security),

    db: AsyncSession = Depends(
        get_db)):

    token = credentials.credentials

    if token in BLACKLISTED_TOKENS:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are logged out. Please login again."
        )

    payload = verify_token(token)

    user_id = payload.get("sub")

    if not user_id:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    result = await db.execute(
        select(User).where(
            User.id == user_id))

    user = result.scalar_one_or_none()

    if not user:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found")

    # Ensure user object is fully loaded before session closes
    await db.refresh(user)

    return user


async def get_current_admin(

    credentials:
    HTTPAuthorizationCredentials = Depends(
        security),

    db: AsyncSession = Depends(
        get_db)):

    user = await get_current_user(
        credentials,
        db)

    if user.role != UserRole.ADMIN:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required")

    return user

async def get_optional_user(

    credentials:
    HTTPAuthorizationCredentials = Depends(
        optional_security),

    db: AsyncSession = Depends(
        get_db)):

    if not credentials:
        return None

    try:

        token = credentials.credentials

        payload = verify_token(token)

        user_id = payload.get("sub")

        if not user_id:
            return None

        result = await db.execute(
            select(User).where(
                User.id == user_id))

        user = result.scalar_one_or_none()

        return user

    except Exception:

        return None


def validate_email(email: str):

    pattern = (
        r"^[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+"
        r"\.[A-Za-z]{2,}$")

    return re.match(
        pattern,
        email)


def validate_phone(
    phone: str):

    pattern = r"^[6-9]\d{9}$"

    return re.match(pattern,phone)