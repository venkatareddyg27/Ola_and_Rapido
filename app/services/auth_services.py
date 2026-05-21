from datetime import datetime, timedelta
import random
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.auth_schema import LoginRequest
from app.models.users import User, OTPLog

from app.core.enums import (
    OTPPurpose,
    UserStatus
)

from app.services.otp import (
    hash_otp,
    verify_otp_hash
)

from app.services.jwt import (
    create_access_token,
    create_refresh_token,
    verify_token
)

from app.schemas.auth_schema import (
    SendOTPRequest,
    VerifyOTPRequest,
    RefreshTokenRequest,
    LogoutRequest,
    RegisterRequest
)


# =========================================================
# SEND OTP
# =========================================================

async def send_otp_service(
    data: SendOTPRequest,
    db: AsyncSession
):

    otp = str(
        random.randint(100000, 999999)
    )

    print("\n===================================")
    print(f"PHONE NUMBER : {data.phone}")
    print(f"OTP           : {otp}")
    print("===================================\n")

    otp_log = OTPLog(
        phone=data.phone,
        otp_hash=hash_otp(otp),
        purpose=OTPPurpose.LOGIN,
        expires_at=datetime.utcnow() + timedelta(minutes=5)
    )

    db.add(otp_log)

    await db.commit()
    await db.refresh(otp_log)

    return {
        "message": "OTP sent successfully"
    }


# =========================================================
# VERIFY OTP
# =========================================================

async def verify_otp_service(
    data: VerifyOTPRequest,
    db: AsyncSession
):

    query = select(OTPLog).where(
        OTPLog.phone == data.phone
    ).order_by(
        OTPLog.created_at.desc()
    )

    result = await db.execute(query)

    otp_log = result.scalars().first()

    if not otp_log:

        raise Exception("OTP not found")

    # CHECK OTP EXPIRY

    if otp_log.expires_at < datetime.utcnow():

        raise Exception("OTP expired")

    # VERIFY OTP

    is_valid = verify_otp_hash(
        data.otp,
        otp_log.otp_hash
    )

    if not is_valid:

        raise Exception("Invalid OTP")

    # MARK OTP AS USED

    otp_log.used_at = datetime.utcnow()

    await db.commit()

    # CHECK USER

    user_query = select(User).where(
        User.phone == data.phone
    )

    user_result = await db.execute(user_query)

    user = user_result.scalars().first()

    # CREATE USER IF NOT EXISTS

    if not user:

        user = User(
            phone=data.phone,
            status=UserStatus.ACTIVE
        )

        db.add(user)

        await db.commit()

        await db.refresh(user)

    # GENERATE TOKENS

    # access_token = create_access_token({
    #     "user_id": str(user.id)
    # })

    # refresh_token = create_refresh_token({
    #     "user_id": str(user.id)
    # })

    # return {
    #     "message": "OTP verified successfully",
    #     "access_token": access_token,
    #     "refresh_token": refresh_token,
    #     "token_type": "bearer",
    #     "user_id": str(user.id)
    # }
    return {
    "message": "OTP verified successfully",
    "verified": True
}

# =========================================================
# REFRESH TOKEN
# =========================================================

async def refresh_token_service(
    refresh_token: str
):

    payload = verify_token(refresh_token)

    if payload.get("type") != "refresh":

        raise Exception("Invalid refresh token")

    user_id = payload.get("user_id")

    new_access_token = create_access_token({
        "user_id": user_id
    })

    new_refresh_token = create_refresh_token({
        "user_id": user_id
    })

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }


# =========================================================
# LOGOUT
# =========================================================

async def logout_service(
    refresh_token: str
):

    return {
        "message": "Logout successful"
    }


# =========================================================
# REGISTER
# =========================================================

async def register_service(
    data: RegisterRequest,
    db: AsyncSession
):

    # CHECK USER EXISTS

    existing_user_query = select(User).where(
        User.phone == data.phone
    )

    existing_user_result = await db.execute(
        existing_user_query
    )

    existing_user = (
        existing_user_result.scalars().first()
    )

    # PHONE ALREADY REGISTERED

    if existing_user and existing_user.first_name:

        raise Exception(
            "Phone number already registered"
        )

    # UPDATE VERIFIED USER

    if existing_user:

        existing_user.first_name = data.first_name
        existing_user.last_name = data.last_name
        existing_user.full_name = data.full_name
        existing_user.email = data.email
        existing_user.profile_photo_url = (
            data.profile_photo_url
        )
        existing_user.role = data.role
        existing_user.status = UserStatus.ACTIVE

        await db.commit()

        await db.refresh(existing_user)

        return {
            "message": "User registered successfully",
            "user_id": str(existing_user.id)
        }

    # CREATE NEW USER

    user = User(
        phone=data.phone,
        first_name=data.first_name,
        last_name=data.last_name,
        full_name=data.full_name,
        email=data.email,
        profile_photo_url=data.profile_photo_url,
        role=data.role,
        status=UserStatus.ACTIVE
    )

    db.add(user)

    await db.commit()

    await db.refresh(user)

    return {
        "message": "User registered successfully",
        "user_id": str(user.id)
    }


async def login_service(
    data: LoginRequest,
    db: AsyncSession
):

    result = await db.execute(
        select(User).where(
            User.phone == data.phone
        )
    )

    user = result.scalar_one_or_none()

    if not user:

        raise Exception("User not found")

    access_token = create_access_token(
        {
            "sub": str(user.id),
            "role": user.role.value
        }
    )

    refresh_token = create_refresh_token(
        {
            "sub": str(user.id)
        }
    )

    return {

        "access_token": access_token,

        "refresh_token": refresh_token,

        "token_type": "bearer",

        "user": {
            "id": str(user.id),
            "phone": user.phone,
            "role": user.role.value
        }
    }

    # =====================================================
    # CHECK USER EXISTS
    # =====================================================

    result = await db.execute(
        select(User).where(
            User.phone == data.phone
        )
    )

    user = result.scalar_one_or_none()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # =====================================================
    # CREATE TOKENS
    # =====================================================

    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "role": user.role.value
        }
    )

    refresh_token = create_refresh_token(
        data={
            "sub": str(user.id)
        }
    )

    # =====================================================
    # RESPONSE
    # =====================================================

    return {

        "access_token": access_token,

        "refresh_token": refresh_token,

        "token_type": "bearer",

        "user": {
            "id": str(user.id),
            "phone": user.phone,
            "role": user.role.value
        }
    }
    # =====================================================
    # CHECK IF PHONE ALREADY EXISTS
    # =====================================================

    existing_user_query = select(User).where(
        User.phone == data.phone
    )

    existing_user_result = await db.execute(
        existing_user_query
    )

    existing_user = (
        existing_user_result.scalars().first()
    )

    if existing_user:

        raise HTTPException(
            status_code=409,
            detail="Phone number already registered"
        )
    # UPDATE EXISTING USER

    if existing_user:

        existing_user.first_name = data.first_name
        existing_user.last_name = data.last_name
        existing_user.full_name = data.full_name
        existing_user.email = data.email
        existing_user.profile_photo_url = (
            data.profile_photo_url
        )
        existing_user.role = data.role
        existing_user.status = UserStatus.ACTIVE

        await db.commit()
        await db.refresh(existing_user)

        return {
            "message": "User updated successfully",
            "user_id": str(existing_user.id)
        }

    # CREATE NEW USER

    user = User(
        phone=data.phone,
        first_name=data.first_name,
        last_name=data.last_name,
        full_name=data.full_name,
        email=data.email,
        profile_photo_url=data.profile_photo_url,
        role=data.role,
        status=UserStatus.ACTIVE
    )

    db.add(user)

    await db.commit()
    await db.refresh(user)

    return {
        "message": "User registered successfully",
        "user_id": str(user.id)
    }