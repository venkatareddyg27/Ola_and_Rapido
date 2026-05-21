# security.py

import re

from datetime import (
    datetime,
    timedelta
)

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

# =========================================================
# PASSWORD HASHING
# =========================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# =========================================================
# HTTP BEARER
# =========================================================

security = HTTPBearer()

# =========================================================
# HASH PASSWORD
# =========================================================

def hash_password(
    text: str
):

    return pwd_context.hash(text)

# =========================================================
# VERIFY PASSWORD
# =========================================================

def verify_password(
    text: str,
    hashed: str
):

    return pwd_context.verify(
        text,
        hashed
    )

# =========================================================
# ACCESS TOKEN
# =========================================================

ACCESS_TOKEN_EXPIRE_MINUTES = (
    settings.ACCESS_TOKEN_EXPIRE_MINUTES
)

def create_access_token(
    data: dict
):

    to_encode = data.copy()

    expire = (
        datetime.utcnow()
        +
        timedelta(
            minutes=
            ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    to_encode.update({
        "exp": expire
    })

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

# =========================================================
# REFRESH TOKEN
# =========================================================

def create_refresh_token(
    user_id: str
):

    payload = {

        "user_id": user_id,

        "exp": (
            datetime.utcnow()
            +
            timedelta(
                days=settings
                .REFRESH_TOKEN_EXPIRE_DAYS
            )
        )
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

# =========================================================
# DECODE ACCESS TOKEN
# =========================================================

def decode_access_token(
    token: str
):

    try:

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[
                settings.ALGORITHM
            ]
        )

        return payload

    except JWTError:

        return None

# =========================================================
# DECODE REFRESH TOKEN
# =========================================================

def decode_refresh_token(
    token: str
):

    return decode_access_token(
        token
    )

# =========================================================
# GET CURRENT USER
# =========================================================

async def get_current_user(
    credentials:
    HTTPAuthorizationCredentials = Depends(
        security
    ),

    db: AsyncSession = Depends(get_db)
):

    token = credentials.credentials

    payload = decode_access_token(
        token
    )

    if not payload:

        raise HTTPException(
            status_code=
            status.HTTP_401_UNAUTHORIZED,

            detail="Invalid token"
        )

    user_id = payload.get("user_id")

    if not user_id:

        raise HTTPException(
            status_code=
            status.HTTP_401_UNAUTHORIZED,

            detail="Invalid token payload"
        )

    result = await db.execute(
        select(User).where(
            User.id == user_id
        )
    )

    user = result.scalars().first()

    if not user:

        raise HTTPException(
            status_code=
            status.HTTP_404_NOT_FOUND,

            detail="User not found"
        )

    return user

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