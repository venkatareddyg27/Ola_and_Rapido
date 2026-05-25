from uuid import UUID
from decimal import Decimal
from datetime import datetime
from typing import (Optional)
from pydantic import (BaseModel,EmailStr,ConfigDict,Field)
from app.core.enums import (
    UserRole,
    UserStatus,
    DriverStatus,
    SubscriptionPlan,
    OTPPurpose)


class UserBase(BaseModel):

    mobile_number: str
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None
    profile_photo_url: Optional[str] = None

class UserCreate(UserBase):

    role: UserRole = (UserRole.CUSTOMER)


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
    model_config = ConfigDict(
        from_attributes=True)


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
    model_config = ConfigDict(
        from_attributes=True)


class DriverProfileBase(BaseModel):

    subscription_plan: (SubscriptionPlan) = SubscriptionPlan.BASIC

class DriverProfileCreate(BaseModel):

    subscription_plan: SubscriptionPlan
    bank_account_number: Optional[str] = None
    ifsc_code: Optional[str] = None
    upi_id: Optional[str] = None
    selfie_url: Optional[str] = None
    license_number: str
    license_front_url: str
    license_back_url: str
    aadhaar_number: str
    aadhaar_front_url: str
    aadhaar_back_url: str
    rc_number: str
    rc_front_url: str
    rc_back_url: str
    insurance_url: str
    pollution_certificate_url: str


class DriverProfileUpdate(BaseModel):

    subscription_plan: SubscriptionPlan
    bank_account_number: Optional[str] = None
    ifsc_code: Optional[str] = None
    upi_id: Optional[str] = None
    selfie_url: Optional[str] = None

class DriverDocumentsUpdate(BaseModel):

    license_number: Optional[str] = None
    license_front_url: Optional[str] = None
    license_back_url: Optional[str] = None
    aadhaar_number: Optional[str] = None
    aadhaar_front_url: Optional[str] = None
    aadhaar_back_url: Optional[str] = None
    rc_number: Optional[str] = None
    rc_front_url: Optional[str] = None
    rc_back_url: Optional[str] = None
    insurance_url: Optional[str] = None
    pollution_certificate_url: Optional[str] = None


class DriverProfileResponse(BaseModel):

    id: UUID
    user_id: UUID
    vehicle_id: Optional[UUID] = None
    subscription_plan: (SubscriptionPlan)
    bank_account_number: Optional[str] = None
    ifsc_code: Optional[str] = None
    upi_id: Optional[str] = None
    selfie_url: Optional[str] = None
    status: DriverStatus
    rating: Decimal
    total_trips: int
    commission_rate: Decimal
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(
        from_attributes=True)


class DriverStatusUpdate(BaseModel):

    status: DriverStatus
    latitude: Decimal
    longitude: Decimal
    heading: Optional[Decimal] = None
    speed: Optional[Decimal] = None


class DriverPerformanceResponse(BaseModel):

    driver_id: UUID
    rating: Decimal
    total_trips: int
    completed_trips: int
    cancelled_trips: int
    acceptance_rate: Decimal
    online_hours: Decimal
    status: DriverStatus


class DriverEarningsResponse(BaseModel):

    total_earnings: Decimal
    total_trips: int
    today_earnings: Decimal
    weekly_earnings: Decimal


class DriverDocumentResponse(BaseModel):

    license_verified: bool
    aadhaar_verified: bool
    bank_verified: bool
    vehicle_verified: bool
    selfie_verified: bool
    admin_remark: Optional[str] = None


class KYCDocumentCreate(BaseModel):

    user_id: UUID
    doc_url: str


class KYCDocumentResponse(BaseModel):

    id: UUID
    user_id: UUID
    doc_url: str
    model_config = ConfigDict(
        from_attributes=True)


class OTPLogCreate(BaseModel):

    user_id: Optional[UUID] = None
    mobile_number: str
    otp_hash: str
    purpose: OTPPurpose
    expires_at: datetime


class OTPLogResponse(BaseModel):

    id: UUID
    user_id: Optional[UUID] = None
    mobile_number: str
    purpose: OTPPurpose
    expires_at: datetime
    used_at: Optional[datetime] = None
    attempts: int
    created_at: datetime
    model_config = ConfigDict(
        from_attributes=True)


class DriverSubscriptionBase(BaseModel):

    plan: SubscriptionPlan
    commission_rate: Optional[Decimal] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    auto_renew: bool = True
    status: str = "active"


class DriverSubscriptionCreate(DriverSubscriptionBase):

    driver_id: UUID


class DriverSubscriptionUpdate(BaseModel):

    plan: Optional[SubscriptionPlan] = None
    commission_rate: Optional[Decimal] = None
    end_date: Optional[datetime] = None
    auto_renew: Optional[bool] = None
    status: Optional[str] = None


class DriverSubscriptionResponse(DriverSubscriptionBase):

    id: UUID
    driver_id: UUID
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(
        from_attributes=True)


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

    mobile_number: str
    first_name: str
    last_name: str
    full_name: str
    email: EmailStr
    profile_photo_url: (str | None) = None
    role: UserRole = Field(
        ...,
        description="""
Supported roles:
- CUSTOMER
- DRIVER
- OWNER
- ADMIN
"""
    )