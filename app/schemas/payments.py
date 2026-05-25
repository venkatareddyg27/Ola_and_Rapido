from datetime import datetime
from decimal import Decimal
from uuid import UUID
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, EmailStr

from app.core.enums import *



class UserBase(BaseModel):
    phone: str
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None
    profile_photo_url: Optional[str] = None
    role: UserRole = UserRole.CUSTOMER


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: UUID
    status: UserStatus
    created_at: datetime

    class Config:
        from_attributes = True


class OTPLogCreate(BaseModel):
    phone: str
    otp_hash: str
    purpose: OTPPurpose
    expires_at: datetime


class OTPLogResponse(BaseModel):
    id: UUID
    phone: str
    purpose: OTPPurpose
    attempts: int
    expires_at: datetime
    used_at: Optional[datetime]

    class Config:
        from_attributes = True


class DriverProfileCreate(BaseModel):
    user_id: UUID
    vehicle_id: Optional[UUID] = None
    subscription_plan: SubscriptionPlan = SubscriptionPlan.BASIC
    commission_rate: Optional[Decimal] = None


class DriverProfileResponse(BaseModel):
    id: UUID
    user_id: UUID
    vehicle_id: Optional[UUID]
    subscription_plan: SubscriptionPlan
    status: DriverStatus
    rating: Decimal
    total_trips: int

    class Config:
        from_attributes = True



class DriverSubscriptionCreate(BaseModel):
    driver_id: UUID
    plan: SubscriptionPlan
    commission_rate: Decimal
    start_date: datetime
    end_date: Optional[datetime]


class DriverSubscriptionResponse(BaseModel):
    id: UUID
    driver_id: UUID
    plan: SubscriptionPlan
    commission_rate: Decimal
    auto_renew: bool
    status: str

    class Config:
        from_attributes = True



class KYCDocumentCreate(BaseModel):
    user_id: UUID
    doc_type: KYCDocType
    doc_url: str


class KYCDocumentResponse(BaseModel):
    id: UUID
    user_id: UUID
    doc_type: KYCDocType
    doc_url: str
    verified_status: KYCStatus

    class Config:
        from_attributes = True


class VehicleCreate(BaseModel):
    owner_id: UUID
    make: str
    model: str
    year: int
    category: VehicleCategory
    registration_number: str


class VehicleResponse(BaseModel):
    id: UUID
    owner_id: UUID
    make: str
    model: str
    year: int
    category: VehicleCategory
    registration_number: str
    status: VehicleStatus

    class Config:
        from_attributes = True



class VehiclePhotoCreate(BaseModel):
    vehicle_id: UUID
    photo_url: str
    angle: VehiclePhotoAngle


class VehiclePhotoResponse(BaseModel):
    id: UUID
    vehicle_id: UUID
    photo_url: str
    angle: VehiclePhotoAngle

    class Config:
        from_attributes = True


class TripCreate(BaseModel):
    customer_id: UUID
    pickup_address: str
    drop_address: str
    pickup_lat: Decimal
    pickup_lng: Decimal
    drop_lat: Decimal
    drop_lng: Decimal
    service_type: ServiceType


class TripResponse(BaseModel):
    id: UUID
    customer_id: UUID
    driver_id: Optional[UUID]
    fare: Optional[Decimal]
    status: TripStatus
    created_at: datetime

    class Config:
        from_attributes = True



class TripLocationCreate(BaseModel):
    trip_id: UUID
    lat: Decimal
    lng: Decimal


class TripLocationResponse(BaseModel):
    id: UUID
    trip_id: UUID
    lat: Decimal
    lng: Decimal

    class Config:
        from_attributes = True



class ParcelCreate(BaseModel):
    trip_id: UUID
    sender_name: str
    sender_phone: str
    receiver_name: str
    receiver_phone: str
    receiver_address: str
    package_type: PackageType


class ParcelResponse(BaseModel):
    id: UUID
    trip_id: UUID
    sender_name: str
    receiver_name: str
    package_type: PackageType

    class Config:
        from_attributes = True



class RentalCreate(BaseModel):
    vehicle_id: UUID
    renter_id: UUID
    owner_id: UUID
    pickup_datetime: datetime
    return_datetime: datetime
    daily_rate: Decimal
    deposit_amount: Decimal


class RentalResponse(BaseModel):
    id: UUID
    vehicle_id: UUID
    renter_id: UUID
    owner_id: UUID
    status: RentalStatus
    total_fare: Optional[Decimal]

    class Config:
        from_attributes = True



class RentalInspectionCreate(BaseModel):
    rental_id: UUID
    inspection_type: InspectionType
    fuel_level: Optional[Decimal]
    odometer_reading: Optional[int]


class RentalInspectionResponse(BaseModel):
    id: UUID
    rental_id: UUID
    inspection_type: InspectionType

    class Config:
        from_attributes = True



class PaymentCreate(BaseModel):
    user_id: UUID
    trip_id: Optional[UUID] = None
    rental_id: Optional[UUID] = None
    amount: Decimal
    method: PaymentMethod


class PaymentResponse(BaseModel):
    id: UUID
    amount: Decimal
    method: PaymentMethod
    status: PaymentStatus
    created_at: datetime

    class Config:
        from_attributes = True



class WalletResponse(BaseModel):
    id: UUID
    user_id: UUID
    balance: Decimal
    currency: str

    class Config:
        from_attributes = True




class WalletTransactionCreate(BaseModel):
    wallet_id: UUID
    type: WalletTransactionType
    amount: Decimal
    reason: str


class WalletTransactionResponse(BaseModel):
    id: UUID
    wallet_id: UUID
    type: WalletTransactionType
    amount: Decimal
    reason: str
    created_at: datetime

    class Config:
        from_attributes = True




class DriverPayoutCreate(BaseModel):
    driver_id: UUID
    amount: Decimal
    method: PayoutMethod


class DriverPayoutResponse(BaseModel):
    id: UUID
    driver_id: UUID
    amount: Decimal
    method: PayoutMethod
    status: PayoutStatus

    class Config:
        from_attributes = True



class RatingCreate(BaseModel):
    trip_id: Optional[UUID]
    rental_id: Optional[UUID]
    rater_id: UUID
    ratee_id: UUID
    score: int
    comment: Optional[str]


class RatingResponse(BaseModel):
    id: UUID
    score: int
    comment: Optional[str]

    class Config:
        from_attributes = True



class DisputeCreate(BaseModel):
    user_id: UUID
    trip_id: Optional[UUID]
    rental_id: Optional[UUID]
    category: DisputeCategory
    description: str


class DisputeResponse(BaseModel):
    id: UUID
    category: DisputeCategory
    status: DisputeStatus
    priority: DisputePriority
    resolution: Optional[str]

    class Config:
        from_attributes = True



class NotificationCreate(BaseModel):
    user_id: UUID
    title: str
    body: str
    type: str


class NotificationResponse(BaseModel):
    id: UUID
    title: str
    body: str
    created_at: datetime

    class Config:
        from_attributes = True



class PromoCodeCreate(BaseModel):
    code: str
    discount_type: DiscountType
    discount_value: Decimal
    valid_from: datetime
    valid_until: datetime


class PromoCodeResponse(BaseModel):
    id: UUID
    code: str
    discount_type: DiscountType
    discount_value: Decimal
    active: bool

    class Config:
        from_attributes = True




class SurgeZoneCreate(BaseModel):
    zone_name: str
    city: str
    polygon: Dict[str, Any]
    multiplier: Decimal


class SurgeZoneResponse(BaseModel):
    id: UUID
    zone_name: str
    city: str
    multiplier: Decimal
    active: bool

    class Config:
        from_attributes = True



class AuditLogResponse(BaseModel):
    id: UUID
    actor_id: UUID
    action: str
    entity_type: str
    entity_id: str
    created_at: datetime

    class Config:
        from_attributes = True