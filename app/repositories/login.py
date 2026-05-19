from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user_model import User


class AuthRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_mobile(self, phone_number: str) -> User | None:
        result = await self.db.execute(
            select(User).where(User.mobile_number == phone_number.strip())
        )
        return result.scalar_one_or_none()