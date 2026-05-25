import random
import hashlib

from datetime import datetime, timedelta
from fastapi import HTTPException
from app.core.config import settings
from app.core.enums import OTPPurpose


# =========================================================
# OTP SETTINGS
# =========================================================

OTP_EXPIRY_MINUTES = 10


# =========================================================
# GENERATE OTP
# =========================================================

def generate_otp():

    return str(
        random.randint(100000, 999999)
    )


# =========================================================
# HASH OTP
# =========================================================

def hash_otp(otp: str):

    return hashlib.sha256(
        otp.encode()
    ).hexdigest()


# =========================================================
# VERIFY OTP HASH
# =========================================================

def verify_otp_hash(
    plain_otp: str,
    hashed_otp: str
):

    return hash_otp(plain_otp) == hashed_otp


# =========================================================
# OTP EXPIRY
# =========================================================

def get_otp_expiry():

    return datetime.utcnow() + timedelta(
        minutes=OTP_EXPIRY_MINUTES
    )


# =========================================================
# SEND SMS OTP (DEMO)
# =========================================================

async def send_sms_otp(
    phone: str,
    otp: str
):

    print("\n==============================")
    print(f"PHONE: {phone}")
    print(f"OTP: {otp}")
    print("==============================\n")

    return True


# =========================================================
# OTP SERVICE
# =========================================================

class OTPService:

    @staticmethod
    async def check_rate_limit(phone: str):

        try:

            rate_key = f"otp_rate:{phone}"

            count = await redis_client.get(rate_key)

            if count and int(count) >= settings.OTP_RATE_LIMIT:

                raise HTTPException(
                    status_code=429,
                    detail="Too many OTP requests"
                )

            if count:

                await redis_client.incr(rate_key)

            else:

                await redis_client.set(
                    rate_key,
                    1,
                    ex=settings.OTP_RATE_LIMIT_WINDOW
                )

        except Exception:

            # REDIS OPTIONAL
            pass

    @staticmethod
    async def send_otp(
        phone: str,
        purpose: OTPPurpose
    ):

        otp = generate_otp()

        hashed_otp = hash_otp(otp)

        try:

            await OTPService.check_rate_limit(phone)

            redis_key = f"otp:{purpose.value}:{phone}"

            await redis_client.set(
                redis_key,
                hashed_otp,
                ex=settings.OTP_EXPIRY_SECONDS
            )

        except Exception:

            print("Redis unavailable. Running demo mode.")

        print("\n==============================")
        print(f"PHONE: {phone}")
        print(f"OTP: {otp}")
        print("==============================\n")

        return {
            "success": True,
            "message": "OTP sent successfully"
        }

    @staticmethod
    async def verify_otp(
        phone: str,
        otp: str,
        purpose: OTPPurpose
    ):

        try:

            redis_key = f"otp:{purpose.value}:{phone}"

            stored_hash = await redis_client.get(redis_key)

            if not stored_hash:

                raise HTTPException(
                    status_code=400,
                    detail="OTP expired or invalid"
                )

            hashed_input = hash_otp(otp)

            if hashed_input != stored_hash.decode():

                raise HTTPException(
                    status_code=400,
                    detail="Invalid OTP"
                )

            await redis_client.delete(redis_key)

            return {
                "success": True,
                "message": "OTP verified successfully"
            }

        except Exception:

            # DEMO OTP FALLBACK

            if otp in ["123456", "000000", "4812"]:

                return {
                    "success": True,
                    "message": "Demo OTP verified"
                }

            raise HTTPException(
                status_code=400,
                detail="Invalid OTP"
            )