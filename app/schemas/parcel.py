# app/schemas/parcel.py

from datetime import datetime
from decimal import Decimal
from typing import Optional, Dict, Any
from uuid import UUID

from pydantic import BaseModel

from app.models.parcel import (
    PackageType,
    WeightTier,
    ParcelStatus,
)


# -------------------------
# CREATE SCHEMA
# -------------------------

class ParcelCreateSchema(BaseModel):

    sender_id: UUID
    receiver_id: Optional[UUID] = None

    package_type: Optional[PackageType] = None
    weight_tier: Optional[WeightTier] = None
    dimensions: Optional[Dict[str, Any]] = None
    description: Optional[str] = None

    is_fragile: Optional[bool] = False

    pickup_address: str
    pickup_latitude: Decimal
    pickup_longitude: Decimal

    pickup_contact_name: Optional[str] = None
    pickup_contact_phone: Optional[str] = None
    pickup_instruction: Optional[str] = None

    delivery_address: str
    delivery_latitude: Decimal
    delivery_longitude: Decimal

    receiver_name: Optional[str] = None
    receiver_phone: Optional[str] = None

    is_cod: Optional[bool] = False
    cod_amount: Optional[Decimal] = None

    expected_delivery_time: Optional[datetime] = None

    payment_method: Optional[str] = None


# -------------------------
# UPDATE SCHEMA
# -------------------------

class ParcelUpdateSchema(BaseModel):

    driver_id: Optional[UUID] = None

    package_type: Optional[PackageType] = None
    weight_tier: Optional[WeightTier] = None
    dimensions: Optional[Dict[str, Any]] = None
    description: Optional[str] = None

    is_fragile: Optional[bool] = None

    pickup_contact_name: Optional[str] = None
    pickup_contact_phone: Optional[str] = None
    pickup_instruction: Optional[str] = None

    receiver_name: Optional[str] = None
    receiver_phone: Optional[str] = None

    is_cod: Optional[bool] = None
    cod_amount: Optional[Decimal] = None

    cod_collected: Optional[bool] = None

    proof_of_pickup_url: Optional[str] = None
    proof_of_delivery_url: Optional[str] = None
    proof_of_delivery_signature: Optional[str] = None

    status: Optional[ParcelStatus] = None

    expected_delivery_time: Optional[datetime] = None

    payment_status: Optional[str] = None


# -------------------------
# RESPONSE SCHEMA
# -------------------------

class ParcelResponseSchema(BaseModel):

    id: UUID
    booking_reference: str

    sender_id: UUID
    receiver_id: Optional[UUID]
    driver_id: Optional[UUID]

    package_type: Optional[PackageType]
    weight_tier: Optional[WeightTier]

    dimensions: Optional[Dict[str, Any]]
    description: Optional[str]

    is_fragile: bool

    pickup_address: str
    pickup_latitude: Decimal
    pickup_longitude: Decimal

    pickup_contact_name: Optional[str]
    pickup_contact_phone: Optional[str]
    pickup_instruction: Optional[str]

    delivery_address: str
    delivery_latitude: Decimal
    delivery_longitude: Decimal

    receiver_name: Optional[str]
    receiver_phone: Optional[str]

    is_cod: bool
    cod_amount: Optional[Decimal]
    cod_collected: bool

    proof_of_pickup_url: Optional[str]
    proof_of_delivery_url: Optional[str]
    proof_of_delivery_signature: Optional[str]

    status: ParcelStatus

    pickup_photo_taken_at: Optional[datetime]
    picked_up_at: Optional[datetime]
    delivered_at: Optional[datetime]

    expected_delivery_time: Optional[datetime]

    base_fare: Optional[Decimal]
    distance_fare: Optional[Decimal]
    cod_fee: Optional[Decimal]
    total_fare: Optional[Decimal]

    payment_method: Optional[str]
    payment_status: Optional[str]

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True