import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.core.enums import ServiceType, TripStatus, PackageType


class TripBase(BaseModel):
    customer_id: uuid.UUID
    driver_id: Optional[uuid.UUID] = None
    pickup_address: Optional[str] = None
    drop_address: Optional[str] = None
    pickup_lat: Optional[Decimal] = None
    pickup_lng: Optional[Decimal] = None
    drop_lat: Optional[Decimal] = None
    drop_lng: Optional[Decimal] = None
    service_type: ServiceType
    fare: Optional[Decimal] = None


class TripCreate(TripBase):
    pass


class TripUpdate(BaseModel):
    driver_id: Optional[uuid.UUID] = None
    pickup_address: Optional[str] = None
    drop_address: Optional[str] = None
    pickup_lat: Optional[Decimal] = None
    pickup_lng: Optional[Decimal] = None
    drop_lat: Optional[Decimal] = None
    drop_lng: Optional[Decimal] = None
    service_type: Optional[ServiceType] = None
    status: Optional[TripStatus] = None
    fare: Optional[Decimal] = None


class TripResponse(TripBase):
    id: uuid.UUID
    status: TripStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TripLocationBase(BaseModel):
    trip_id: uuid.UUID
    lat: Optional[Decimal] = None
    lng: Optional[Decimal] = None


class TripLocationCreate(TripLocationBase):
    pass


class TripLocationUpdate(BaseModel):
    lat: Optional[Decimal] = None
    lng: Optional[Decimal] = None


class TripLocationResponse(TripLocationBase):
    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


class ParcelBase(BaseModel):
    trip_id: uuid.UUID
    sender_name: str
    sender_phone: str
    receiver_name: str
    receiver_phone: str
    receiver_address: str
    package_type: PackageType
    weight_kg: Optional[Decimal] = None
    cod_amount: Decimal = Decimal("0.00")
    pod_photo_url: Optional[str] = None
    pod_signature_url: Optional[str] = None
    pod_otp: Optional[str] = None
    status: str = "pending"


class ParcelCreate(ParcelBase):
    pass


class ParcelUpdate(BaseModel):
    sender_name: Optional[str] = None
    sender_phone: Optional[str] = None
    receiver_name: Optional[str] = None
    receiver_phone: Optional[str] = None
    receiver_address: Optional[str] = None
    package_type: Optional[PackageType] = None
    weight_kg: Optional[Decimal] = None
    cod_amount: Optional[Decimal] = None
    pod_photo_url: Optional[str] = None
    pod_signature_url: Optional[str] = None
    pod_otp: Optional[str] = None
    status: Optional[str] = None


class ParcelResponse(ParcelBase):
    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)