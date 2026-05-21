

from uuid import UUID
from decimal import Decimal
from datetime import datetime
from typing import Optional, List
from pydantic import Field
from pydantic import (
    BaseModel,
    EmailStr,
    ConfigDict
)

from app.core.enums import (
    UserRole,
    UserStatus,
    DriverStatus,
    SubscriptionPlan,
    OTPPurpose,
)



# =========================================================
# USER SCHEMAS
# =========================================================

class UserBase(BaseModel):
    phone: str

    email: Optional[EmailStr] = None

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None

    profile_photo_url: Optional[str] = None


class UserCreate(UserBase):
    role: UserRole = UserRole.CUSTOMER

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None

    profile_photo_url: Optional[str] = None

    status: Optional[UserStatus] = None


class UserResponse(UserBase):
    id: UUID

    role: UserRole
    status: UserStatus

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =========================================================
# DRIVER LOCATION SCHEMAS
# =========================================================

class DriverLocationBase(BaseModel):
    latitude: Decimal
    longitude: Decimal

    heading: Optional[Decimal] = None
    speed: Optional[Decimal] = None

    is_active: bool = True


class DriverLocationCreate(DriverLocationBase):
    driver_id: UUID


class DriverLocationUpdate(BaseModel):
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None

    heading: Optional[Decimal] = None
    speed: Optional[Decimal] = None

    is_active: Optional[bool] = None


class DriverLocationResponse(DriverLocationBase):
    id: UUID

    driver_id: UUID

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =========================================================
# DRIVER PROFILE SCHEMAS
# =========================================================

class DriverProfileBase(BaseModel):
    subscription_plan: SubscriptionPlan = SubscriptionPlan.BASIC

    commission_rate: Optional[Decimal] = None

    status: DriverStatus = DriverStatus.INACTIVE

    rating: Optional[Decimal] = Decimal("5.0")

    total_trips: int = 0


class DriverProfileCreate(DriverProfileBase):
    user_id: UUID

    vehicle_id: Optional[UUID] = None


class DriverProfileUpdate(BaseModel):
    subscription_plan: Optional[SubscriptionPlan] = None

    commission_rate: Optional[Decimal] = None

    status: Optional[DriverStatus] = None

    rating: Optional[Decimal] = None

    total_trips: Optional[int] = None

    vehicle_id: Optional[UUID] = None


class DriverProfileResponse(DriverProfileBase):
    id: UUID

    user_id: UUID

    vehicle_id: Optional[UUID] = None

    locations: List[DriverLocationResponse] = []

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =========================================================
# KYC DOCUMENT SCHEMAS
# =========================================================

class KYCDocumentCreate(BaseModel):
    user_id: UUID

    doc_url: str


class KYCDocumentResponse(BaseModel):
    id: UUID

    user_id: UUID

    doc_url: str

    model_config = ConfigDict(from_attributes=True)


# =========================================================
# OTP LOG SCHEMAS
# =========================================================

class OTPLogCreate(BaseModel):
    user_id: Optional[UUID] = None

    phone: str

    otp_hash: str

    purpose: OTPPurpose 

    expires_at: datetime


class OTPLogResponse(BaseModel):
    id: UUID

    user_id: Optional[UUID] = None

    phone: str

    purpose: OTPPurpose

    expires_at: datetime

    used_at: Optional[datetime] = None

    attempts: int

    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =========================================================
# DRIVER SUBSCRIPTION SCHEMAS
# =========================================================

class DriverSubscriptionBase(BaseModel):
    plan: SubscriptionPlan

    commission_rate: Optional[Decimal] = None

    start_date: datetime

    end_date: Optional[datetime] = None

    auto_renew: bool = True

    status: str = "active"


class DriverSubscriptionCreate(
    DriverSubscriptionBase
):
    driver_id: UUID


class DriverSubscriptionUpdate(BaseModel):
    plan: Optional[SubscriptionPlan] = None

    commission_rate: Optional[Decimal] = None

    end_date: Optional[datetime] = None

    auto_renew: Optional[bool] = None

    status: Optional[str] = None


class DriverSubscriptionResponse(
    DriverSubscriptionBase
):
    id: UUID

    driver_id: UUID

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


    # =========================================================
# AUTH SCHEMAS
# =========================================================

class SendOTPRequest(BaseModel):
    mobile_number: str


class VerifyOTPRequest(BaseModel):
    mobile_number: str
    otp: str



class RefreshTokenRequest(BaseModel):
    refresh_token: str


class LogoutRequest(BaseModel):
    refresh_token: str


class RegisterRequest(BaseModel):

    phone: str

    first_name: str

    last_name: str

    full_name: str

    email: EmailStr

    profile_photo_url: str | None = None

    role: UserRole = Field(
        ...,
        description="""
The registration system supports three user roles:
- CUSTOMER: Regular riders who book trips and rentals
- DRIVER: Service providers who complete trips
- OWNER: Vehicle owners who list vehicles for rental
""",
        example="customer"
    )
