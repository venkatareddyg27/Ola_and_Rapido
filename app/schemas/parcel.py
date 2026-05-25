from datetime import datetime
from decimal import Decimal
import uuid
from pydantic import BaseModel, Field

from app.core.enums import (
    ParcelStatus,
    ParcelType,
    ParcelPriority,
    VehicleCategory,
    TripStatus,
    ProofType,
    DeliveryAttemptStatus,
    PaymentStatus,
    FeedbackType,
)


class ORMBase(BaseModel):
    model_config = {"from_attributes": True}


class ParcelCreate(BaseModel):
    pickup_address: str
    pickup_lat: Decimal
    pickup_lng: Decimal

    delivery_address: str
    delivery_lat: Decimal
    delivery_lng: Decimal

    parcel_type: ParcelType = ParcelType.PACKAGE
    priority: ParcelPriority = ParcelPriority.NORMAL
    
    sender_name: str
    receiver_name: str
    receiver_phone: str
    receiver_address: str

    package_type: str
    weight_kg: Decimal


class ParcelUpdate(BaseModel):
    receiver_id: int | None = None
    driver_id: int | None = None
    status: ParcelStatus | None = None
    picked_up_at: datetime | None = None
    delivered_at: datetime | None = None
    cancelled_at: datetime | None = None


class ParcelBookingResponse(BaseModel):
    message: str
    trip_id: uuid.UUID
    parcel_id: uuid.UUID
    distance_km: Decimal
    delivery_charge: Decimal
    vehicle_category: VehicleCategory
    trip_status: TripStatus
    parcel_status: str
    
    
class ParcelItemBase(BaseModel):
    name: str
    description: str | None = None
    quantity: int = 1
    weight_kg: Decimal | None = None
    declared_value: Decimal | None = None


class ParcelItemCreate(ParcelItemBase):
    parcel_id: int


class ParcelItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    quantity: int | None = None
    weight_kg: Decimal | None = None
    declared_value: Decimal | None = None


class ParcelItemResponse(ParcelItemBase, ORMBase):
    id: int
    parcel_id: int
    created_at: datetime

class ParcelTrackingBase(BaseModel):
    latitude: Decimal
    longitude: Decimal
    location_text: str | None = None
    note: str | None = None


class ParcelTrackingCreate(ParcelTrackingBase):
    parcel_id: int


class ParcelTrackingUpdate(BaseModel):
    latitude: Decimal | None = None
    longitude: Decimal | None = None
    location_text: str | None = None
    note: str | None = None


class ParcelTrackingResponse(ParcelTrackingBase, ORMBase):
    id: int
    parcel_id: int
    recorded_at: datetime   
class ParcelTrackingBase(BaseModel):
    latitude: Decimal
    longitude: Decimal
    location_text: str | None = None
    note: str | None = None


class ParcelTrackingCreate(ParcelTrackingBase):
    parcel_id: int


class ParcelTrackingUpdate(BaseModel):
    latitude: Decimal | None = None
    longitude: Decimal | None = None
    location_text: str | None = None
    note: str | None = None


class ParcelTrackingResponse(ParcelTrackingBase, ORMBase):
    id: int
    parcel_id: int
    recorded_at: datetime   
class ParcelStatusHistoryBase(BaseModel):
    old_status: ParcelStatus | None = None
    new_status: ParcelStatus
    changed_by: int | None = None
    note: str | None = None


class ParcelStatusHistoryCreate(ParcelStatusHistoryBase):
    parcel_id: int


class ParcelStatusHistoryUpdate(BaseModel):
    note: str | None = None


class ParcelStatusHistoryResponse(ParcelStatusHistoryBase, ORMBase):
    id: int
    parcel_id: int
    changed_at: datetime
class ParcelProofBase(BaseModel):
    proof_type: ProofType
    proof_url: str | None = None
    otp_code: str | None = None
    signed_by: str | None = None
    uploaded_by: int | None = None


class ParcelProofCreate(ParcelProofBase):
    parcel_id: int


class ParcelProofUpdate(BaseModel):
    proof_url: str | None = None
    otp_code: str | None = None
    signed_by: str | None = None


class ParcelProofResponse(ParcelProofBase, ORMBase):
    id: int
    parcel_id: int
    created_at: datetime

class ParcelDeliveryAttemptBase(BaseModel):
    attempt_number: int
    status: DeliveryAttemptStatus
    reason: str | None = None
    attempted_by: int | None = None
    next_attempt_at: datetime | None = None


class ParcelDeliveryAttemptCreate(ParcelDeliveryAttemptBase):
    parcel_id: int


class ParcelDeliveryAttemptUpdate(BaseModel):
    status: DeliveryAttemptStatus | None = None
    reason: str | None = None
    next_attempt_at: datetime | None = None


class ParcelDeliveryAttemptResponse(ParcelDeliveryAttemptBase, ORMBase):
    id: int
    parcel_id: int
    attempted_at: datetime

class ParcelPricingBase(BaseModel):
    base_price: Decimal = Decimal("0.00")
    distance_price: Decimal = Decimal("0.00")
    weight_price: Decimal = Decimal("0.00")
    priority_fee: Decimal = Decimal("0.00")
    discount_amount: Decimal = Decimal("0.00")
    tax_amount: Decimal = Decimal("0.00")
    total_price: Decimal
    currency: str = "INR"
    payment_status: PaymentStatus = PaymentStatus.PENDING


class ParcelPricingCreate(ParcelPricingBase):
    parcel_id: int


class ParcelPricingUpdate(BaseModel):
    base_price: Decimal | None = None
    distance_price: Decimal | None = None
    weight_price: Decimal | None = None
    priority_fee: Decimal | None = None
    discount_amount: Decimal | None = None
    tax_amount: Decimal | None = None
    total_price: Decimal | None = None
    payment_status: PaymentStatus | None = None


class ParcelPricingResponse(ParcelPricingBase, ORMBase):
    id: int
    parcel_id: int
    created_at: datetime

class ParcelFeedbackBase(BaseModel):
    user_id: int
    feedback_type: FeedbackType | None = None
    rating: int | None = Field(default=None, ge=1, le=5)
    message: str | None = None


class ParcelFeedbackCreate(ParcelFeedbackBase):
    parcel_id: int


class ParcelFeedbackUpdate(BaseModel):
    feedback_type: FeedbackType | None = None
    rating: int | None = Field(default=None, ge=1, le=5)
    message: str | None = None


class ParcelFeedbackResponse(ParcelFeedbackBase, ORMBase):
    id: int
    parcel_id: int
    created_at: datetime