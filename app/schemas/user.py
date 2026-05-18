# schemas/user_schema.py

from decimal import Decimal
from enum import Enum
from datetime import date, datetime
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, EmailStr, Field, ConfigDict

from Ola_and_Rapido.app.core.enums import DriverStatus, KYCStatus, LoyaltyTier


class UserRole(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    DRIVER = "DRIVER"
    STORE_MANAGER = "STORE_MANAGER"


class Gender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"


class UserBase(BaseModel):
    phone_number: str = Field(..., max_length=15)
    email: Optional[EmailStr] = None
    full_name: str = Field(..., max_length=255)
    profile_photo_url: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    emergency_contacts: List[Dict[str, Any]] = []
    preferred_language: str = "en"
    notification_settings: Dict[str, Any] = {}


class UserCreate(UserBase):
    role: UserRole
    hashed_password: Optional[str] = None
    firebase_uid: Optional[str] = None


class UserUpdate(BaseModel):
    phone_number: Optional[str] = Field(None, max_length=15)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=255)

    hashed_password: Optional[str] = None
    firebase_uid: Optional[str] = None

    is_phone_verified: Optional[bool] = None
    is_active: Optional[bool] = None
    is_blocked: Optional[bool] = None
    blocked_reason: Optional[str] = None

    profile_photo_url: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None

    emergency_contacts: Optional[List[Dict[str, Any]]] = None
    preferred_language: Optional[str] = None
    notification_settings: Optional[Dict[str, Any]] = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    phone_number: str
    email: Optional[EmailStr]
    full_name: str
    role: UserRole

    firebase_uid: Optional[str]

    is_phone_verified: bool
    is_active: bool
    is_blocked: bool
    blocked_reason: Optional[str]

    profile_photo_url: Optional[str]
    date_of_birth: Optional[date]
    gender: Optional[Gender]

    emergency_contacts: List[Dict[str, Any]]
    preferred_language: str
    notification_settings: Dict[str, Any]

    created_at: datetime
    updated_at: datetime
    last_login_at: Optional[datetime]
    
# =========================================================
# CUSTOMER PROFILE SCHEMAS
# =========================================================

class CustomerProfileCreate(BaseModel):
    user_id: int
    saved_addresses: Optional[List[Dict[str, Any]]] = []


class CustomerProfileUpdate(BaseModel):
    kyc_status: Optional[KYCStatus] = None
    kyc_rejection_reason: Optional[str] = None
    kyc_expires_at: Optional[datetime] = None
    saved_addresses: Optional[List[Dict[str, Any]]] = None
    average_rating: Optional[Decimal] = None
    loyalty_points: Optional[int] = None
    loyalty_tier: Optional[LoyaltyTier] = None


class CustomerProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int

    kyc_status: KYCStatus
    kyc_rejection_reason: Optional[str]
    kyc_approved_at: Optional[datetime]
    kyc_expires_at: Optional[datetime]

    saved_addresses: List[Dict[str, Any]]

    total_rides: int
    total_parcels: int
    total_rentals: int

    lifetime_spent: Decimal
    average_rating: Decimal

    loyalty_points: int
    loyalty_tier: LoyaltyTier

    created_at: datetime
    updated_at: datetime

# =========================================================
# DRIVER PROFILE SCHEMAS
# =========================================================

class DriverProfileCreate(BaseModel):
    user_id: int


class DriverProfileUpdate(BaseModel):
    current_vehicle_id: Optional[int] = None

    is_online: Optional[bool] = None

    current_status: Optional[DriverStatus] = None

    break_mode_until: Optional[datetime] = None

    current_city: Optional[str] = None

    current_zone: Optional[str] = None

    cancellation_rate: Optional[Decimal] = None

    acceptance_rate: Optional[Decimal] = None

    average_rating: Optional[Decimal] = None

    wallet_balance: Optional[Decimal] = None

    bank_account_name: Optional[str] = None

    bank_account_number: Optional[str] = None

    bank_ifsc: Optional[str] = None

    upi_id: Optional[str] = None

    dl_verified: Optional[bool] = None

    rc_verified: Optional[bool] = None

    puc_verified: Optional[bool] = None

    insurance_verified: Optional[bool] = None

    background_check_completed: Optional[bool] = None

    last_latitude: Optional[Decimal] = None

    last_longitude: Optional[Decimal] = None

    last_location_update: Optional[datetime] = None


class DriverProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

    user_id: int

    current_vehicle_id: Optional[int]

    is_online: bool

    current_status: DriverStatus

    break_mode_until: Optional[datetime]

    current_city: Optional[str]

    current_zone: Optional[str]

    total_earnings: Decimal

    total_rides_completed: int

    total_parcels_delivered: int

    cancellation_rate: Decimal

    acceptance_rate: Decimal

    average_rating: Decimal

    wallet_balance: Decimal

    bank_account_name: Optional[str]

    bank_account_number: Optional[str]

    bank_ifsc: Optional[str]

    upi_id: Optional[str]

    dl_verified: bool

    rc_verified: bool

    puc_verified: bool

    insurance_verified: bool

    background_check_completed: bool

    last_latitude: Optional[Decimal]

    last_longitude: Optional[Decimal]

    last_location_update: Optional[datetime]

    created_at: datetime

    updated_at: datetime
    
# =========================================================
# CAR OWNER PROFILE SCHEMAS
# =========================================================

class CarOwnerProfileCreate(BaseModel):
    user_id: int

    pan_number: Optional[str] = None

    bank_account_name: Optional[str] = None

    bank_account_number: Optional[str] = None

    bank_ifsc: Optional[str] = None

    upi_id: Optional[str] = None


class CarOwnerProfileUpdate(BaseModel):
    kyc_status: Optional[KYCStatus] = None

    pan_verified: Optional[bool] = None

    pan_number: Optional[str] = None

    aadhaar_verified: Optional[bool] = None

    bank_account_verified: Optional[bool] = None

    bank_account_name: Optional[str] = None

    bank_account_number: Optional[str] = None

    bank_ifsc: Optional[str] = None

    upi_id: Optional[str] = None

    average_rating: Optional[Decimal] = None


class CarOwnerProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

    user_id: int

    kyc_status: KYCStatus

    pan_verified: bool

    pan_number: Optional[str]

    aadhaar_verified: bool

    aadhaar_tokenized_id: Optional[str]

    bank_account_verified: bool

    bank_account_name: Optional[str]

    bank_account_number: Optional[str]

    bank_ifsc: Optional[str]

    upi_id: Optional[str]

    total_listings: int

    total_rentals_completed: int

    total_earnings: Decimal

    average_rating: Decimal

    created_at: datetime

    updated_at: datetime