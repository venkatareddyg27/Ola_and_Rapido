import random

import hashlib
 
from fastapi import HTTPException
 
from app.core.redis import redis_client

from app.core.config import settings

from app.core.enums import OTPPurpose
 
 
class OTPService:
 
    @staticmethod

    def generate_otp() -> str:
 
        return str(

            random.randint(100000, 999999)

        )

 
    @staticmethod

    def hash_otp(otp: str) -> str:
 
        return hashlib.sha256(

            otp.encode()

        ).hexdigest()

 
    @staticmethod

    async def check_rate_limit(phone: str):
 
        rate_key = f"otp_rate:{phone}"
 
        count = await redis_client.get(rate_key)
 
        if count and int(count) >= settings.OTP_RATE_LIMIT:
 
            raise HTTPException(

                status_code=429,

                detail="Too many OTP requests. Try again later."

            )
 
        if count:
 
            await redis_client.incr(rate_key)
 
        else:
 
            await redis_client.set(

                rate_key,

                1,

                ex=settings.OTP_RATE_LIMIT_WINDOW

            )
 
    @staticmethod

    async def send_otp(

        phone: str,

        purpose: OTPPurpose

    ):
 
        try:

            await OTPService.check_rate_limit(phone)

            otp = OTPService.generate_otp()


            hashed_otp = OTPService.hash_otp(otp)

            redis_key = f"otp:{purpose.value}:{phone}"

            await redis_client.set(

                redis_key,

                hashed_otp,

                ex=settings.OTP_EXPIRY_SECONDS

            )
            print(f"OTP for {phone}: {otp}")
 
            return {

                "success": True,

                "message": "OTP sent successfully"

            }
 
        except Exception:

 
            print("Redis unavailable. Demo mode enabled.")
 
            return {

                "success": True,

                "message": "Demo OTP mode",

                "demo_otp": "123456"

            }
 
 
    # =====================================================

    # VERIFY OTP

    # =====================================================
 
    @staticmethod

    async def verify_otp(

        phone: str,

        otp: str,

        purpose: OTPPurpose

    ):
 
        redis_key = f"otp:{purpose.value}:{phone}"
 
        # GET STORED HASH

        stored_hash = await redis_client.get(redis_key)
 
        if not stored_hash:
 
            raise HTTPException(

                status_code=400,

                detail="OTP expired or invalid"

            )
 
        # HASH INPUT OTP

        hashed_input = OTPService.hash_otp(otp)
 
        # VERIFY HASH

        if hashed_input != stored_hash.decode():
 
            raise HTTPException(

                status_code=400,

                detail="Invalid OTP"

            )
 
        # DELETE OTP AFTER SUCCESS

        await redis_client.delete(redis_key)
 
        return {

            "success": True,

            "message": "OTP verified successfully"

        }
 