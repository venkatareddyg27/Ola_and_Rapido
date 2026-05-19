import random
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums import UserRole
from app.repositories.mobile import otp_repo
from app.repositories.mobile import OTPUserRepository


class OTPService:

    async def send_otp(
        self,
        mobile: str,
       
        db: AsyncSession,
    ):
        mobile = mobile.strip()
        role = UserRole.CUSTOMER

        user_repo = OTPUserRepository(db)
        user = await user_repo.get_user_by_phone(mobile)

        if user:
            if user.is_blocked:
                raise HTTPException(
                    status_code=403,
                    detail=f"User blocked: {user.blocked_reason}",
                )

            return {
                "message": "User already exists",
                "user_id": user.id,
                
            }

        otp = str(random.randint(100000, 999999))

        try:
            await otp_repo.send(mobile, otp)
        except Exception as e:
            raise HTTPException(status_code=429, detail=str(e))

        print(f"🔥 OTP for {mobile}: {otp}")

        return {
            "message": "OTP sent successfully",
            "mobile_number": mobile,
            
        }

    async def resend_otp(
        self,
        mobile: str,
        db: AsyncSession,
    ):
        mobile = mobile.strip()
        role = UserRole.CUSTOMER

        user_repo = OTPUserRepository(db)
        user = await user_repo.get_user_by_phone(mobile)

        if user:
            if user.is_blocked:
                raise HTTPException(
                    status_code=403,
                    detail=f"User blocked: {user.blocked_reason}",
                )

            return {
                "message": "User already exists",
                "user_id": user.id,
                
            }

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
            "role": role.value,
            
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

        if user and user.is_blocked:
            raise HTTPException(
                status_code=403,
                detail=f"User blocked: {user.blocked_reason}",
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

        if user:
            return {
                "message": "User already exists",
                "user_id": user.id,
                
            }

        user = await user_repo.create_user_with_phone(
            phone_number=mobile,
            role=role,
        )

        return {
            "message": "User created successfully",
            "user_id": user.id,
            
        }


otp_service = OTPService()