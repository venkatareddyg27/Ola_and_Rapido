import random
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums import UserRole
from app.core.security import create_access_token
from app.repositories.mobile import otp_repo, OTPUserRepository


class OTPService:

    async def send_otp(
        self,
        mobile: str,
        db: AsyncSession,
    ):
        mobile = mobile.strip()

        user_repo = OTPUserRepository(db)
        user = await user_repo.get_user_by_phone(mobile)

        if user and not user.is_active:
            raise HTTPException(
                status_code=403,
                detail="User blocked or inactive",
            )

        otp = str(random.randint(100000, 999999))

        try:
            await otp_repo.send(mobile, otp)
        except Exception as e:
            raise HTTPException(status_code=429, detail=str(e))

        print(f"🔥 OTP for {mobile}: {otp}")

        return {
            "message": "OTP sent successfully",
            "mobile_number": mobile,
            "is_existing_user": bool(user),
        }

    async def resend_otp(
        self,
        mobile: str,
        db: AsyncSession,
    ):
        mobile = mobile.strip()

        user_repo = OTPUserRepository(db)
        user = await user_repo.get_user_by_phone(mobile)

        if user and not user.is_active:
            raise HTTPException(
                status_code=403,
                detail="User blocked or inactive",
            )

        otp = str(random.randint(100000, 999999))

        try:
            await otp_repo.resend(mobile, otp)
        except Exception as e:
            error_message = str(e)

            if "Resend limit exceeded" in error_message:
                await user_repo.block_mobile_number(
                    mobile,
                    reason="Too many OTP resend attempts",
                )

            raise HTTPException(status_code=400, detail=error_message)

        print(f"🔁 Resend OTP for {mobile}: {otp}")

        return {
            "message": "OTP resent successfully",
            "mobile_number": mobile,
            "is_existing_user": bool(user),
        }

    async def verify_otp(
        self,
        mobile: str,
        otp: str,
        db: AsyncSession,
    ):
        mobile = mobile.strip()
        otp = otp.strip()
        role = UserRole.CUSTOMER

        user_repo = OTPUserRepository(db)
        user = await user_repo.get_user_by_phone(mobile)

        if user and not user.is_active:
            raise HTTPException(
                status_code=403,
                detail="User blocked or inactive",
            )

        try:
            await otp_repo.verify(mobile, otp)
        except Exception as e:
            error_message = str(e)

            if "Max attempts exceeded" in error_message:
                await user_repo.block_mobile_number(
                    mobile,
                    reason="Too many invalid OTP attempts",
                )

            raise HTTPException(status_code=400, detail=error_message)

        if not user:
            user = await user_repo.create_user_with_phone(
                phone_number=mobile,
                role=role,
            )
            is_new_user = True
        else:
            is_new_user = False

        user_role = user.role.value if hasattr(user.role, "value") else user.role

        access_token = create_access_token({
            "sub": str(user.id),
            "role": user_role,
            "type": "DB_USER",
        })

        refresh_token = create_access_token({
            "sub": str(user.id),
            "role": user_role,
            "type": "DB_USER",
        })

        profile_completed = bool(user.full_name and user.email)

        return {
            "message": "Profile created successfully" if is_new_user else "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user_id": user.id,
            "mobile_number": user.mobile_number,
            "role": user_role,
            "is_new_user": is_new_user,
            "profile_completed": profile_completed,
            "next_screen": "DASHBOARD" if profile_completed else "CREATE_PROFILE",
        }


otp_service = OTPService()