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
    VerifyOTPRequest,
    RegisterRequest,
    LoginRequest
)

from app.core.enums import (
    OTPPurpose,
    UserRole
)

from app.services.otp import (
    hash_otp,
    verify_otp_hash
)

from app.core.security import (

    create_access_token,

    create_refresh_token
)

# =========================================================
# LOGIN SERVICE
# =========================================================

async def login_service(

    data: LoginRequest,

    db: AsyncSession
):

    otp = str(
        random.randint(
            100000,
            999999
        )
    )

    print("\n===================================")

    print(
        f"PHONE NUMBER : {data.phone}"
    )

    print(
        f"OTP           : {otp}"
    )

    print(
        "===================================\n"
    )

    otp_log = OTPLog(

        phone=data.phone,

        otp_hash=hash_otp(
            otp
        ),

        purpose=
        OTPPurpose.LOGIN,

        expires_at=

        datetime.utcnow()

        +

        timedelta(
            minutes=5
        )
    )

    db.add(otp_log)

    await db.commit()

    await db.refresh(otp_log)

    return {

        "success":
        True,

        "message":
        "OTP sent successfully",

        "phone":
        data.phone
    }

# =========================================================
# VERIFY OTP SERVICE
# =========================================================

async def verify_otp_service(

    data: VerifyOTPRequest,

    db: AsyncSession
):

    query = select(OTPLog).where(

        OTPLog.phone ==
        data.phone

    ).order_by(

        OTPLog.created_at.desc()
    )

    result = await db.execute(
        query
    )

    otp_log = (
        result.scalars().first()
    )

    if not otp_log:

        raise HTTPException(

            status_code=404,

            detail=
            "OTP not found"
        )

    if otp_log.expires_at < datetime.utcnow():

        raise HTTPException(

            status_code=400,

            detail=
            "OTP expired"
        )

    is_valid = verify_otp_hash(

        data.otp,

        otp_log.otp_hash
    )

    if not is_valid:

        raise HTTPException(

            status_code=400,

            detail=
            "Invalid OTP"
        )

    # =====================================================
    # MARK OTP USED
    # =====================================================

    otp_log.used_at = (
        datetime.utcnow()
    )

    await db.commit()

    # =====================================================
    # GET USER
    # =====================================================

    user_query = select(User).where(

        User.mobile_number ==
        data.phone
    )

    user_result = await db.execute(
        user_query
    )

    user = (
        user_result.scalars().first()
    )

    # =====================================================
    # CREATE USER
    # =====================================================

    if not user:

        user = User(

            mobile_number=
            data.phone,

            role=
            UserRole.CUSTOMER,

            is_active=True,

            is_verified=True
        )

        db.add(user)

        await db.commit()

        await db.refresh(user)

    # =====================================================
    # CREATE TOKENS
    # =====================================================

    access_token = (
        create_access_token(

            str(user.id),

            str(user.role)
        )
    )

    refresh_token = (
        create_refresh_token(

            str(user.id),

            str(user.role)
        )
    )

    return {

        "message":
        "OTP verified successfully",

        "verified":
        True,

        "access_token":
        access_token,

        "refresh_token":
        refresh_token,

        "token_type":
        "bearer",

        "user": {

            "id":
            str(user.id),

            "phone":
            user.mobile_number,

            "role":
            str(user.role)
        }
    }

# =========================================================
# LOGOUT SERVICE
# =========================================================

async def logout_service(
    refresh_token: str
):

    return {

        "message":
        "Logout successful"
    }

# =========================================================
# REGISTER SERVICE
# =========================================================

async def register_service(

    data: RegisterRequest,

    db: AsyncSession
):

    result = await db.execute(

        select(User).where(

            User.mobile_number ==
            data.phone
        )
    )

    user = (
        result.scalar_one_or_none()
    )

    if not user:

        raise HTTPException(

            status_code=404,

            detail=
            "User not found. Please login first."
        )

    user.first_name = (
        data.first_name
    )

    user.last_name = (
        data.last_name
    )

    user.full_name = (
        data.full_name
    )

    user.email = (
        data.email
    )

    user.profile_photo_url = (
        data.profile_photo_url
    )

    user.role = (
        data.role
    )

    user.is_active = True

    user.is_verified = True

    await db.commit()

    await db.refresh(user)

    return {

        "message":
        "User registered successfully",

        "user": {

            "id":
            str(user.id),

            "phone":
            user.mobile_number,

            "first_name":
            user.first_name,

            "last_name":
            user.last_name,

            "full_name":
            user.full_name,

            "email":
            user.email,

            "profile_photo_url":
            user.profile_photo_url,

            "role":
            str(user.role)
        }
    }