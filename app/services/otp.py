import random
import hashlib
from datetime import datetime, timedelta
from fastapi import HTTPException
from app.core.enums import OTPPurpose

OTP_EXPIRY_MINUTES = 10
otp_storage = {}


def generate_otp():
    return str(random.randint(100000, 999999))


def hash_otp(otp: str):
    return hashlib.sha256(otp.encode()).hexdigest()


def verify_otp_hash(plain_otp: str, hashed_otp: str):
    return hash_otp(plain_otp) == hashed_otp


def get_otp_expiry():
    return datetime.utcnow() + timedelta(minutes=OTP_EXPIRY_MINUTES)


async def send_sms_otp(phone: str, otp: str):
    print("\n==============================")
    print(f"PHONE: {phone}")
    print(f"OTP: {otp}")
    print("==============================\n")
    return True


class OTPService:

    @staticmethod
    async def send_otp(phone: str, purpose: OTPPurpose):
        otp = generate_otp()
        hashed_otp = hash_otp(otp)
        expiry = get_otp_expiry()

        storage_key = f"{purpose.value}:{phone}"

        otp_storage[storage_key] = {
            "otp": hashed_otp,
            "expires_at": expiry
        }

        print("\n==============================")
        print(f"PHONE: {phone}")
        print(f"OTP: {otp}")
        print(f"PURPOSE: {purpose.value}")
        print("==============================\n")

        return {
            "success": True,
            "message": "OTP sent successfully"
        }

    @staticmethod
    async def verify_otp(phone: str, otp: str, purpose: OTPPurpose):
        storage_key = f"{purpose.value}:{phone}"
        otp_data = otp_storage.get(storage_key)

        if not otp_data:
            raise HTTPException(status_code=400, detail="OTP expired or invalid")

        if datetime.utcnow() > otp_data["expires_at"]:
            del otp_storage[storage_key]
            raise HTTPException(status_code=400, detail="OTP expired")

        hashed_input = hash_otp(otp)

        if hashed_input != otp_data["otp"]:
            raise HTTPException(status_code=400, detail="Invalid OTP")

        del otp_storage[storage_key]

        return {
            "success": True,
            "message": "OTP verified successfully"
        }