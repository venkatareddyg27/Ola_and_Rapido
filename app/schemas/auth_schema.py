from pydantic import (BaseModel,EmailStr,field_validator,Field)
from app.core.enums import UserRole


class LoginRequest(BaseModel):
    phone: str
    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if not value.startswith("+91"):
            raise ValueError("Phone number must start with +91")

        mobile = value[3:]
        if not mobile.isdigit():
            raise ValueError("Phone number must contain digits only")
        if len(mobile) != 10:
            raise ValueError("Phone number must be exactly 10 digits")
        return value


class VerifyOTPRequest(BaseModel):
    phone: str
    otp: str
    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if not value.startswith("+91"):
            raise ValueError("Phone number must start with +91")
        mobile = value[3:]
        if not mobile.isdigit():
            raise ValueError("Phone number must contain digits only")
        if len(mobile) != 10:
            raise ValueError("Phone number must be exactly 10 digits")

        return value


class RegisterRequest(BaseModel):
    phone: str
    first_name: str
    last_name: str
    full_name: str
    email: EmailStr
    profile_photo_url: str | None = None
    role: UserRole = Field(default=UserRole.CUSTOMER,examples=["CUSTOMER"])

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if not value.startswith("+91"):
            raise ValueError("Phone number must start with +91")
        mobile = value[3:]
        if not mobile.isdigit():
            raise ValueError("Phone number must contain digits only")
        if len(mobile) != 10:
            raise ValueError("Phone number must be exactly 10 digits")
        return value