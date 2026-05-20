from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from app.schemas.auth_schema import (
    SendOTPRequest,
    VerifyOTPRequest,
    RefreshTokenRequest,
    LogoutRequest,
    RegisterRequest
)

from app.services.auth_service import (
    send_otp_service,
    verify_otp_service,
    refresh_token_service,
    logout_service,
    register_service
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# =========================================================
# SEND OTP
# =========================================================

@router.post("/send-otp")
async def send_otp(
    data: SendOTPRequest,
    db: AsyncSession = Depends(get_db)
):

    try:

        return await send_otp_service(
            data=data,
            db=db
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# =========================================================
# VERIFY OTP
# =========================================================

@router.post("/verify-otp")
async def verify_otp(
    data: VerifyOTPRequest,
    db: AsyncSession = Depends(get_db)
):

    try:

        return await verify_otp_service(
            data=data,
            db=db
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# =========================================================
# REFRESH TOKEN
# =========================================================

@router.post("/refresh")
async def refresh_token(
    data: RefreshTokenRequest
):

    try:

        return await refresh_token_service(
            refresh_token=data.refresh_token
        )

    except Exception as e:

        raise HTTPException(
            status_code=401,
            detail=str(e)
        )


# =========================================================
# LOGOUT
# =========================================================

@router.post("/logout")
async def logout(
    data: LogoutRequest
):

    try:

        return await logout_service(
            refresh_token=data.refresh_token
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# =========================================================
# REGISTER
# =========================================================

@router.post("/register")
async def register(
    data: RegisterRequest,
    db: AsyncSession = Depends(get_db)
):

    try:

        return await register_service(
            data=data,
            db=db
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )