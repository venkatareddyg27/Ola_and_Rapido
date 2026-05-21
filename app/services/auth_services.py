# =========================================================
# app/services/auth_service.py
# =========================================================

import random

from datetime import (
    datetime,
    timedelta
)

from fastapi import (
    HTTPException
)

from sqlalchemy import (
    select
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from app.models.user_models import (
    User,
    OTPLog
)

from app.schemas.auth_schema import (
    SendOTPRequest,
    VerifyOTPRequest,
    RefreshTokenRequest,
    LogoutRequest,
    RegisterRequest,
    LoginRequest
)

from app.core.enums import (
    OTPPurpose
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

    # =====================================================
    # GET OTP
    # =====================================================

    query = select(OTPLog).where(
        OTPLog.phone == data.phone
    ).order_by(
        OTPLog.created_at.desc()
    )

    result = await db.execute(query)

    otp_log = result.scalars().first()

    if not otp_log:

        raise HTTPException(
            status_code=404,
            detail="OTP not found"
        )

    # =====================================================
    # CHECK EXPIRY
    # =====================================================

    if otp_log.expires_at < datetime.utcnow():

        raise HTTPException(
            status_code=400,
            detail="OTP expired"
        )

    # =====================================================
    # VERIFY OTP
    # =====================================================

    is_valid = verify_otp_hash(
        data.otp,
        otp_log.otp_hash
    )

    if not is_valid:

        raise HTTPException(
            status_code=400,
            detail="Invalid OTP"
        )

    # =====================================================
    # MARK USED
    # =====================================================

    otp_log.used_at = datetime.utcnow()

    await db.commit()

    # =====================================================
    # FIND USER
    # =====================================================

    user_query = select(User).where(
        User.mobile_number == data.phone
    )

    user_result = await db.execute(user_query)

    user = user_result.scalars().first()

    # =====================================================
    # CREATE USER IF NOT EXISTS
    # =====================================================

    if not user:

        user = User(
            mobile_number=data.phone,
            is_active=True,
            is_verified=True
        )

        db.add(user)

        await db.commit()

        await db.refresh(user)

    # =====================================================
    # GENERATE TOKENS
    # =====================================================

    access_token = create_access_token({
        "sub": str(user.id),
        "role": user.role
    })

    refresh_token = create_refresh_token({
        "sub": str(user.id)
    })

    # =====================================================
    # RESPONSE
    # =====================================================

    return {

        "message": "OTP verified successfully",

        "verified": True,

        "access_token": access_token,

        "refresh_token": refresh_token,

        "token_type": "bearer",

        "user": {

            "id": str(user.id),

            "phone": user.mobile_number,

            "role": user.role
        }
    }


# =========================================================
# REFRESH TOKEN
# =========================================================

async def refresh_token_service(
    refresh_token: str
):

    payload = verify_token(refresh_token)

    if payload.get("type") != "refresh":

        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )

    user_id = payload.get("sub")

    new_access_token = create_access_token({
        "sub": user_id
    })

    new_refresh_token = create_refresh_token({
        "sub": user_id
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

    # =====================================================
    # CHECK EXISTING USER
    # =====================================================

    existing_user_query = select(User).where(
        User.mobile_number == data.phone
    )

    existing_user_result = await db.execute(
        existing_user_query
    )

    existing_user = (
        existing_user_result.scalars().first()
    )

    # =====================================================
    # UPDATE EXISTING USER
    # =====================================================

    if existing_user:

        existing_user.full_name = data.full_name

        existing_user.email = data.email

        existing_user.profile_photo_url = (
            data.profile_photo_url
        )

        existing_user.role = data.role

        existing_user.is_active = True

        existing_user.is_verified = True

        await db.commit()

        await db.refresh(existing_user)

        return {

            "message": "User updated successfully",

            "user_id": str(existing_user.id)
        }

    # =====================================================
    # CREATE USER
    # =====================================================

    user = User(

        mobile_number=data.phone,

        full_name=data.full_name,

        email=data.email,

        profile_photo_url=data.profile_photo_url,

        role=data.role,

        is_active=True,

        is_verified=True
    )

    db.add(user)

    await db.commit()

    await db.refresh(user)

    return {

        "message": "User registered successfully",

        "user_id": str(user.id)
    }


# =========================================================
# LOGIN
# =========================================================

async def login_service(
    data: LoginRequest,
    db: AsyncSession
):

    # =====================================================
    # FIND USER
    # =====================================================

    result = await db.execute(

        select(User).where(
            User.mobile_number == data.phone
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

    access_token = create_access_token({

        "sub": str(user.id),

        "role": user.role
    })

    refresh_token = create_refresh_token({

        "sub": str(user.id)
    })

    # =====================================================
    # RESPONSE
    # =====================================================

    return {

        "access_token": access_token,

        "refresh_token": refresh_token,

        "token_type": "bearer",

        "user": {

            "id": str(user.id),

            "phone": user.mobile_number,

            "role": user.role
        }
    }