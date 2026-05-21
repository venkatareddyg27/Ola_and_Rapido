

from pydantic import BaseModel, EmailStr, Field
from app.core.enums import OTPPurpose, UserRole


# =========================================================
# SEND OTP
# =========================================================

class SendOTPRequest(BaseModel):

    phone: str

    purpose: OTPPurpose


# =========================================================
# VERIFY OTP
# =========================================================

class VerifyOTPRequest(BaseModel):

    phone: str

    otp: str


# =========================================================
# REGISTER
# =========================================================

class RegisterRequest(BaseModel):

    phone: str

    first_name: str

    last_name: str

    full_name: str

    email: EmailStr

    profile_photo_url: str | None = None

    role: UserRole = Field(
        ...,
        example="CUSTOMER"
    )


# =========================================================
# LOGIN
# =========================================================

class LoginRequest(BaseModel):

    phone: str


# =========================================================
# REFRESH TOKEN
# =========================================================

class RefreshTokenRequest(BaseModel):

    refresh_token: str


# =========================================================
# LOGOUT
# =========================================================

class LogoutRequest(BaseModel):

    refresh_token: str