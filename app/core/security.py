from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer
)

from jose import JWTError, jwt
from passlib.context import CryptContext

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import settings
from app.core.database import get_db

from app.models.users import User
from app.core.enums import UserRole


# =========================================================
# HTTP BEARER AUTH
# =========================================================

security = HTTPBearer()

optional_security = HTTPBearer(
    auto_error=False
)


# =========================================================
# PASSWORD HASHING
# =========================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:

    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# =========================================================
# JWT CONFIG
# =========================================================

SECRET_KEY = settings.SECRET_KEY

ALGORITHM = settings.ALGORITHM

ACCESS_TOKEN_EXPIRE_MINUTES = 60

REFRESH_TOKEN_EXPIRE_DAYS = 7


# =========================================================
# CREATE ACCESS TOKEN
# =========================================================

def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
):

    to_encode = data.copy()

    expire = datetime.utcnow() + (
        expires_delta
        or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({
        "exp": expire,
        "type": "access"
    })

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


# =========================================================
# CREATE REFRESH TOKEN
# =========================================================

def create_refresh_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
):

    to_encode = data.copy()

    expire = datetime.utcnow() + (
        expires_delta
        or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

    to_encode.update({
        "exp": expire,
        "type": "refresh"
    })

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


# =========================================================
# VERIFY TOKEN
# =========================================================

def verify_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )


# =========================================================
# GET CURRENT USER
# =========================================================

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):

    token = credentials.credentials

    payload = verify_token(token)

    user_id = payload.get("user_id")

    if not user_id:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    result = await db.execute(
        select(User).where(User.id == user_id)
    )

    user = result.scalar_one_or_none()

    if not user:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if user.status.name != "ACTIVE":

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive"
        )

    return user


# =========================================================
# GET CURRENT ADMIN
# =========================================================

async def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):

    token = credentials.credentials

    payload = verify_token(token)

    user_id = payload.get("user_id")

    if not user_id:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    result = await db.execute(
        select(User).where(User.id == user_id)
    )

    user = result.scalar_one_or_none()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user.role != UserRole.ADMIN:

        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return user


# =========================================================
# OPTIONAL USER AUTH
# =========================================================

async def get_optional_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        optional_security
    ),
    db: AsyncSession = Depends(get_db)
):

    if not credentials:

        return None

    token = credentials.credentials

    try:

        payload = verify_token(token)

        user_id = payload.get("user_id")

        if not user_id:

            return None

        result = await db.execute(
            select(User).where(User.id == user_id)
        )

        user = result.scalar_one_or_none()

        return user

    except Exception:

        return None