# =========================================================
# app/repositories/mobile.py
# =========================================================

from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_models import User, BlockedUser
from app.core.enums import UserRole


OTP_STORE = {}


class OTPRepository:

    async def send(self, mobile: str, otp: str):
        mobile = mobile.strip()

        OTP_STORE[mobile] = {
            "otp": otp,
            "expires_at": datetime.utcnow() + timedelta(minutes=5),
            "attempts_left": 3,
            "resend_count": 0,
        }

        print("AFTER SEND OTP_STORE =", OTP_STORE)

    async def resend(self, mobile: str, otp: str):
        mobile = mobile.strip()

        existing = OTP_STORE.get(mobile)

        if not existing:
            raise Exception("Send OTP first before resend")

        if existing["resend_count"] >= 3:
            raise Exception("Resend limit exceeded")

        existing["otp"] = otp
        existing["expires_at"] = datetime.utcnow() + timedelta(minutes=5)
        existing["attempts_left"] = 3
        existing["resend_count"] += 1

        print("AFTER RESEND OTP_STORE =", OTP_STORE)

    async def verify(self, mobile: str, otp: str):
        mobile = mobile.strip()
        otp = otp.strip()

        data = OTP_STORE.get(mobile)

        if not data:
            raise Exception("OTP not found. Send OTP first")

        if datetime.utcnow() > data["expires_at"]:
            await self.delete(mobile)
            raise Exception("OTP expired")

        if data["otp"] != otp:
            data["attempts_left"] -= 1

            if data["attempts_left"] <= 0:
                await self.delete(mobile)
                raise Exception("Max attempts exceeded")

            raise Exception(f"Invalid OTP. Attempts left: {data['attempts_left']}")

        await self.delete(mobile)
        return True

    async def delete(self, mobile: str):
        OTP_STORE.pop(mobile.strip(), None)


otp_repo = OTPRepository()


class OTPUserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_phone(self, phone_number: str):
        result = await self.db.execute(
            select(User).where(User.mobile_number == phone_number.strip())
        )
        return result.scalar_one_or_none()

    async def create_user_with_phone(self, phone_number: str, role: UserRole):
        role_value = role.value if hasattr(role, "value") else str(role)

        user = User(
            mobile_number=phone_number.strip(),
            full_name=None,
            email=None,
            role=role_value,
            is_verified=True,
            is_active=True,
        )

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return user
    async def block_mobile_number(self, phone_number: str, reason: str):
        user = await self.get_user_by_phone(phone_number)

        if not user:
            role_value = (
                UserRole.CUSTOMER.value
                if hasattr(UserRole.CUSTOMER, "value")
                else str(UserRole.CUSTOMER)
            )

            user = User(
                mobile_number=phone_number.strip(),
                full_name="",
                role=role_value,
                is_verified=False,
                is_active=False,
            )
            self.db.add(user)
            await self.db.flush()
        else:
            user.is_active = False

        blocked_user = BlockedUser(
            user_id=user.id,
            blocked_reason=reason,
        )
        self.db.add(blocked_user)

        await self.db.commit()
        await self.db.refresh(user)

        return user
