from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import random
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.security import create_access_token
from app.repositories.login import AuthRepository
from app.utils.validators import validate_mobile
from app.core.dependencies import get_current_user
from app.models.user_models import User

router = APIRouter(prefix="/auth", tags=["Auth"])

# TEMP OTP storage
otp_store = {}


# ==========================
# SEND OTP ROUTER
# ==========================
@router.post("/send-otp")
async def send_otp(
    mobile: str,
    db: AsyncSession = Depends(get_db),
):
    validate_mobile(mobile)

    auth_repo = AuthRepository(db)
    user = await auth_repo.get_user_by_mobile(mobile)

    # ✅ User must exist
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Register first with mobile number"
        )

    otp = str(random.randint(100000, 999999))

    otp_store[mobile] = {
        "otp": otp,
        "expires_at": datetime.utcnow() + timedelta(minutes=5),
    }

    print(f"OTP for {mobile}: {otp}")

    return {
        "message": "OTP sent successfully"
    }


# ==========================
# VERIFY OTP ROUTER
# ==========================
@router.post("/verify-otp")
async def verify_otp(
    mobile: str,
    otp: str,
    db: AsyncSession = Depends(get_db),
):
    validate_mobile(mobile)

    saved_otp = otp_store.get(mobile)

    if not saved_otp:
        raise HTTPException(status_code=400, detail="OTP not requested")

    if saved_otp["expires_at"] < datetime.utcnow():
        otp_store.pop(mobile, None)
        raise HTTPException(status_code=400, detail="OTP expired")

    if saved_otp["otp"] != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    auth_repo = AuthRepository(db)
    user = await auth_repo.get_user_by_mobile(mobile)

    # ✅ Double safety check
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Register first with mobile number"
        )

    otp_store.pop(mobile, None)

    role = user.role.value if hasattr(user.role, "value") else user.role

    access_token = create_access_token({
        "sub": str(user.id),
        "role": role,
        "type": "DB_USER"
    })

    refresh_token = create_access_token({
        "sub": str(user.id),
        "role": role,
        "type": "DB_USER"
    })

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user_id": user.id,
        "role": role,
    }


# ==========================
# CURRENT USER
# ==========================
@router.get("/me")
async def me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "phone_number": current_user.phone_number,
        "role": current_user.role.value if hasattr(current_user.role, "value") else current_user.role,
    }