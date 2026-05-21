from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth_schema import LoginRequest
from app.core.database import get_db

from app.core.security import (
    security,
    get_current_user
)

from app.schemas.auth_schema import (
    SendOTPRequest,
    VerifyOTPRequest,
    RefreshTokenRequest,
    LogoutRequest,
    RegisterRequest
)

from app.services.auth_services import (
    send_otp_service,
    verify_otp_service,
    refresh_token_service,
    logout_service,
    register_service,
    login_service
)

from app.models.user_models import User


# =========================================================
# ROUTER
# =========================================================

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

@router.post(
    "/verify-otp",
    summary="Verify OTP"
)
async def verify_otp(
    data: VerifyOTPRequest,
    db: AsyncSession = Depends(get_db)
):
    try:
        response = await verify_otp_service(
            data=data,
            db=db
        )
        return {
            "success": True,
            "message": "OTP verified successfully",
            "verified": True
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.post(
    "/register",
    summary="Register User",
    description="""
AVAILABLE ROLES:

- CUSTOMER → Regular riders who book trips and rentals
- DRIVER → Service providers who complete trips
- OWNER → Vehicle owners who list vehicles for rental
    """
)
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

@router.post("/login")
async def login(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):

    return await login_service(
        data=data,
        db=db
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
# CURRENT USER
# =========================================================

@router.get("/me")
async def get_me(
    current_user: User = Depends(get_current_user)
):

    return {
        "message": "Authorized Successfully",
        "user_id": str(current_user.id),
        "phone": current_user.phone,
        "role": str(current_user.role)
    }