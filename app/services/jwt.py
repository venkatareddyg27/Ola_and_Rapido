from datetime import datetime, timedelta
from typing import Optional

from jose import jwt, JWTError

from fastapi import (
    Depends,
    HTTPException,
    status
)

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import settings
from app.core.database import get_db
from app.models.users import User


# =========================================================
# JWT CONFIG
# =========================================================

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


# =========================================================
# SWAGGER AUTH
# =========================================================

security = HTTPBearer()


# =========================================================
# CREATE ACCESS TOKEN
# =========================================================

def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
):

    to_encode = data.copy()

    expire = datetime.utcnow() + (
        expires_delta or
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
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
        expires_delta or
        timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
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
            detail="Invalid or Expired Token"
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
            status_code=401,
            detail="Invalid token payload"
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

    return user