from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_models import User


class ProfileRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_or_update_profile(
        self,
        user: User,
        full_name: str,
        email: str,
        gender: str | None = None,
        profile_photo_url: str | None = None,
    ):
        user.full_name = full_name
        user.email = email
        user.gender = gender
        user.profile_photo_url = profile_photo_url

        await self.db.commit()
        await self.db.refresh(user)

        return user