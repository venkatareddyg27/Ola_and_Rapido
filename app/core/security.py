# security.py

import re

from datetime import (
    datetime,
    timedelta
)

from typing import Optional

from jose import (
    jwt,
    JWTError
)

from passlib.context import (
    CryptContext
)

from fastapi import (
    Depends,
    HTTPException,
    status
)

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from sqlalchemy import (
    select
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.core.config import (
    settings
)

from app.core.database import (
    get_db
)

from app.models.user_models import (
    User
)

from app.core.enums import (
    UserRole
)

# =========================================================
# PASSWORD HASHING
# =========================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# =========================================================
# HTTP BEARER AUTH
# =========================================================

security = HTTPBearer()

optional_security = HTTPBearer(
    auto_error=False
)

# =========================================================
# JWT CONFIG
# =========================================================

SECRET_KEY = settings.SECRET_KEY

ALGORITHM = settings.ALGORITHM

ACCESS_TOKEN_EXPIRE_MINUTES = (
    settings.ACCESS_TOKEN_EXPIRE_MINUTES
)

REFRESH_TOKEN_EXPIRE_DAYS = (
    settings.REFRESH_TOKEN_EXPIRE_DAYS
)

# =========================================================
# HASH PASSWORD
# =========================================================

def hash_password(
    password: str
) -> str:

    return pwd_context.hash(password)

# =========================================================
# VERIFY PASSWORD
# =========================================================

def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:

    return pwd_context.verify(
        plain_password,
        hashed_password
    )

# =========================================================
# CREATE ACCESS TOKEN
# =========================================================

def create_access_token(
    data: dict,
    expires_delta: Optional[
        timedelta
    ] = None
):

    to_encode = data.copy()

    expire = datetime.utcnow() + (

        expires_delta

        or timedelta(
            minutes=
            ACCESS_TOKEN_EXPIRE_MINUTES
        )
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
    expires_delta: Optional[
        timedelta
    ] = None
):

    to_encode = data.copy()

    expire = datetime.utcnow() + (

        expires_delta

        or timedelta(
            days=
            REFRESH_TOKEN_EXPIRE_DAYS
        )
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

def verify_token(
    token: str
):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:

        raise HTTPException(
            status_code=
            status.HTTP_401_UNAUTHORIZED,

            detail=
            "Invalid or expired token"
        )

# =========================================================
# DECODE ACCESS TOKEN
# =========================================================

def decode_access_token(
    token: str
):

    return verify_token(token)

# =========================================================
# DECODE REFRESH TOKEN
# =========================================================

def decode_refresh_token(
    token: str
):

    return verify_token(token)

# =========================================================
# GET CURRENT USER
# =========================================================

async def get_current_user(
    credentials:
    HTTPAuthorizationCredentials = Depends(
        security
    ),

    db: AsyncSession = Depends(
        get_db
    )
):

    token = credentials.credentials

    payload = verify_token(token)

    user_id = payload.get(
        "user_id"
    )

    if not user_id:

        raise HTTPException(
            status_code=
            status.HTTP_401_UNAUTHORIZED,

            detail=
            "Invalid token payload"
        )

    result = await db.execute(
        select(User).where(
            User.id == user_id
        )
    )

    user = result.scalar_one_or_none()

    if not user:

        raise HTTPException(
            status_code=
            status.HTTP_404_NOT_FOUND,

            detail="User not found"
        )

    return user

# =========================================================
# GET CURRENT ADMIN
# =========================================================

async def get_current_admin(
    credentials:
    HTTPAuthorizationCredentials = Depends(
        security
    ),

    db: AsyncSession = Depends(
        get_db
    )
):

    user = await get_current_user(
        credentials,
        db
    )

    if user.role != UserRole.ADMIN:

        raise HTTPException(
            status_code=
            status.HTTP_403_FORBIDDEN,

            detail=
            "Admin access required"
        )

    return user

# =========================================================
# OPTIONAL USER
# =========================================================

async def get_optional_user(
    credentials:
    HTTPAuthorizationCredentials = Depends(
        optional_security
    ),

    db: AsyncSession = Depends(
        get_db
    )
):

    if not credentials:
        return None

    try:

        token = credentials.credentials

        payload = verify_token(token)

        user_id = payload.get(
            "user_id"
        )

        if not user_id:
            return None

        result = await db.execute(
            select(User).where(
                User.id == user_id
            )
        )

        user = result.scalar_one_or_none()

        return user

    except Exception:

        return None

# =========================================================
# EMAIL VALIDATION
# =========================================================

def validate_email(
    email: str
):

    pattern = (
        r"^[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+"
        r"\.[A-Za-z]{2,}$"
    )

    return re.match(
        pattern,
        email
    )

# =========================================================
# PHONE VALIDATION
# =========================================================

def validate_phone(
    phone: str
):

    pattern = r"^[6-9]\d{9}$"

    return re.match(
        pattern,
        phone
    )