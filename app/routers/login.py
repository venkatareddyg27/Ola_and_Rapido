from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.security import verify_password, create_access_token
from app.repositories.login import AuthRepository
from app.utils.validators import validate_mobile
from app.core.config import settings
from app.core.dependencies import get_current_user
from app.models.user_model import User

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    validate_mobile(form_data.username)

    # 1. SuperAdmin login from .env only
    if (
        form_data.username == settings.SUPERADMIN_MOBILE
        and form_data.password == settings.SUPERADMIN_PASSWORD
    ):
        access_token = create_access_token({
            "sub": "superadmin",
            "role": "SUPER_ADMIN",
            "type": "ENV_SUPER_ADMIN"
        })
        refresh_token = create_access_token({
            "sub": "superadmin",
            "role": "SUPER_ADMIN",
            "type": "ENV_SUPER_ADMIN"
        })

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "role": "SUPER_ADMIN",
        }

    # 2. Normal users login from DB
    auth_repo = AuthRepository(db)
    user = await auth_repo.get_user_by_mobile(form_data.username)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

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

@router.get("/me")
async def me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "phone_number": current_user.phone_number,
        "role": current_user.role.value,
    }