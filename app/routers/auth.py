from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from fastapi.security import (
    HTTPAuthorizationCredentials
)

from app.core.database import (
    get_db
)

from app.core.security import (

    get_current_user,

    security,

    blacklist_token
)

from app.schemas.auth_schema import (

    VerifyOTPRequest,

    LoginRequest,

    RegisterRequest
)

from app.services.auth_services import (

    verify_otp_service,

    login_service,

    register_service
)

from app.models.user_models import (
    User
)


# =========================================================
# AUTH ROUTER
# =========================================================

router = APIRouter(

    prefix="/auth",

    tags=["Authentication"]

)


# =========================================================
# PROFILE ROUTER
# =========================================================

profile_router = APIRouter(

    prefix="/profile",

    tags=["Profile"]

)


# =========================================================
# LOGIN
# =========================================================

@router.post("/login")
async def login(

    data: LoginRequest,

    db: AsyncSession = Depends(
        get_db
    )

):

    try:

        return await login_service(

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

    db: AsyncSession = Depends(
        get_db
    )

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
# LOGOUT
# =========================================================

@router.post("/logout")
async def logout(

    credentials:
    HTTPAuthorizationCredentials = Depends(
        security
    )

):

    token = (
        credentials.credentials
    )

    blacklist_token(
        token
    )

    return {

        "success": True,

        "message":
        "Logged out successfully. Please login again."

    }


# =========================================================
# CURRENT USER
# =========================================================

@router.get("/me")
async def get_me(

    current_user: User = Depends(
        get_current_user
    )

):

    return {

        "message":
        "Authorized Successfully",

        "user_id":
        str(current_user.id),

        "full_name":
        current_user.full_name,

        "mobile_number":
        current_user.mobile_number,

        "email":
        current_user.email,

        "role":
        str(current_user.role)

    }


# =========================================================
# UPDATE PROFILE
# =========================================================

@profile_router.post("/update")
async def update_profile(

    data: RegisterRequest,

    db: AsyncSession = Depends(
        get_db
    )

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