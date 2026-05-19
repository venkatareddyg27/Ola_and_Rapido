# =========================================================
# app/schemas/auth_schema.py
# =========================================================

from pydantic import (
    BaseModel,
    EmailStr,
    ConfigDict
)

from typing import Optional
from datetime import datetime

from app.core.enums import (
    UserRoleEnum,
    GenderEnum,
    DeviceTypeEnum,
    OTPPurposeEnum,
    LoginStatusEnum,
    BlockStatusEnum,
    PermissionEnum,
    RoleNameEnum,
)


# =========================================================
# USER SCHEMAS
# =========================================================

class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    mobile_number: str
    gender: Optional[GenderEnum] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    mobile_number: Optional[str] = None
    gender: Optional[GenderEnum] = None
    profile_photo_url: Optional[str] = None


class UserResponse(UserBase):
    id: int
    role: UserRoleEnum
    profile_photo_url: Optional[str]
    is_active: bool
    is_verified: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# LOGIN SCHEMAS
# =========================================================

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# =========================================================
# USER SESSION SCHEMAS
# =========================================================

class UserSessionCreate(BaseModel):
    user_id: int
    access_token: str
    refresh_token: str
    device_info: Optional[str]
    ip_address: Optional[str]
    expires_at: datetime


class UserSessionResponse(UserSessionCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# USER DEVICE SCHEMAS
# =========================================================

class UserDeviceCreate(BaseModel):
    user_id: int
    device_id: str
    device_type: DeviceTypeEnum
    fcm_token: Optional[str] = None
    app_version: Optional[str] = None


class UserDeviceResponse(UserDeviceCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# USER ROLE SCHEMAS
# =========================================================

class UserRoleCreate(BaseModel):
    user_id: int
    role_name: RoleNameEnum


class UserRoleResponse(UserRoleCreate):
    id: int
    assigned_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# USER PERMISSION SCHEMAS
# =========================================================

class UserPermissionCreate(BaseModel):
    permission_name: PermissionEnum
    description: Optional[str] = None


class UserPermissionResponse(UserPermissionCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# ROLE PERMISSION SCHEMAS
# =========================================================

class RolePermissionCreate(BaseModel):
    role_name: RoleNameEnum
    permission_id: int


class RolePermissionResponse(RolePermissionCreate):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# OTP VERIFICATION SCHEMAS
# =========================================================

class OTPRequest(BaseModel):
    mobile_number: str
    purpose: OTPPurposeEnum


class OTPVerifyRequest(BaseModel):
    mobile_number: str
    otp_code: str


class OTPVerificationResponse(BaseModel):
    id: int
    mobile_number: str
    purpose: OTPPurposeEnum
    is_verified: bool
    expires_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# PASSWORD RESET SCHEMAS
# =========================================================

class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str


class PasswordResetTokenResponse(BaseModel):
    id: int
    user_id: int
    reset_token: str
    expires_at: datetime
    is_used: bool

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# LOGIN HISTORY SCHEMAS
# =========================================================

class LoginHistoryResponse(BaseModel):
    id: int
    user_id: int
    ip_address: Optional[str]
    device_info: Optional[str]
    login_status: LoginStatusEnum
    logged_in_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# BLOCKED USER SCHEMAS
# =========================================================

class BlockUserRequest(BaseModel):
    user_id: int
    blocked_reason: str
    blocked_by_admin_id: int
    blocked_until: Optional[datetime] = None


class BlockedUserResponse(BaseModel):
    id: int
    user_id: int
    blocked_reason: Optional[str]
    blocked_by_admin_id: Optional[int]
    blocked_until: Optional[datetime]
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )