from uuid import UUID
from decimal import Decimal
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from app.core.enums import (
    UserRole,
    UserStatus,
    DriverStatus,
    SubscriptionPlan,
    OTPPurpose,
)

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

    class Config:
        from_attributes = True


class DriverProfileBase(BaseModel):
    subscription_plan: SubscriptionPlan = SubscriptionPlan.BASIC
    commission_rate: Optional[Decimal] = None
    status: DriverStatus = DriverStatus.OFFLINE
    rating: Optional[Decimal] = 5.0
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


class DriverProfileResponse(DriverProfileBase):
    id: UUID
    user_id: UUID
    vehicle_id: Optional[UUID] = None

    class Config:
        from_attributes = True


class KYCDocumentCreate(BaseModel):
    user_id: UUID
    doc_url: str


class KYCDocumentResponse(BaseModel):
    id: UUID
    user_id: UUID
    doc_url: str

    class Config:
        from_attributes = True


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

    class Config:
        from_attributes = True


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

    class Config:
        from_attributes = True