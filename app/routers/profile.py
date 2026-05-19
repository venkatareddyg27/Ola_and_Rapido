from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user_model import User
from app.schemas.profile import CreateProfileRequest
from app.repositories.profile import ProfileRepository

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.post("/create")
async def create_profile(
    request: CreateProfileRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = ProfileRepository(db)

    user = await repo.create_or_update_profile(
        user=current_user,
        full_name=request.full_name,
        email=request.email,
        profile_photo_url=request.profile_photo_url,
    )

    return {
        "message": "Profile saved successfully",
        "profile_completed": True,
        "next_screen": "DASHBOARD",
        "user_id": user.id,
        "phone_number": user.phone_number,
        "full_name": user.full_name,
        "email": user.email,
        "profile_photo_url": user.profile_photo_url,
        "role": user.role.value,
    }