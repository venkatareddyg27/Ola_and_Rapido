import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import (
    BaseModel,
    ConfigDict)

from app.core.enums import (
    ServiceType,
    TripStatus,
    PackageType,
    VehicleCategory)


class TripEstimateRequest(BaseModel):

    pickup_lat: Decimal

    pickup_lng: Decimal

    drop_lat: Decimal

    drop_lng: Decimal

    vehicle_category: VehicleCategory


class TripEstimateResponse(BaseModel):

    vehicle_category: VehicleCategory

    distance_km: Decimal

    estimated_fare: Decimal

    fare_breakdown: dict


class TripBase(BaseModel):

    pickup_address: Optional[
        str
    ] = None

    drop_address: Optional[
        str
    ] = None

    pickup_lat: Optional[
        Decimal
    ] = None

    pickup_lng: Optional[
        Decimal
    ] = None

    drop_lat: Optional[
        Decimal
    ] = None

    drop_lng: Optional[
        Decimal
    ] = None

    service_type: ServiceType


class TripCreate(TripBase):

    pickup_lat: Decimal

    pickup_lng: Decimal

    drop_lat: Decimal

    drop_lng: Decimal

    vehicle_category: VehicleCategory


class TripUpdate(BaseModel):

    pickup_address: Optional[
        str
    ] = None

    drop_address: Optional[
        str
    ] = None

    pickup_lat: Optional[
        Decimal
    ] = None

    pickup_lng: Optional[
        Decimal
    ] = None

    drop_lat: Optional[
        Decimal
    ] = None

    drop_lng: Optional[
        Decimal
    ] = None

    service_type: Optional[
        ServiceType
    ] = None

    status: Optional[
        TripStatus
    ] = None


class TripResponse(TripBase):

    id: uuid.UUID

    customer_id: uuid.UUID

    driver_id: Optional[
        uuid.UUID
    ] = None

    status: TripStatus

    fare: Optional[
        Decimal
    ] = None

    estimated_distance: Optional[
        Decimal
    ] = None

    estimated_fare: Optional[
        Decimal
    ] = None

    vehicle_category: Optional[
        VehicleCategory
    ] = None

    ride_otp: Optional[
        str
    ] = None

    cancel_reason: Optional[
        str
    ] = None

    cancelled_at: Optional[
        datetime
    ] = None

    started_at: Optional[
        datetime
    ] = None

    completed_at: Optional[
        datetime
    ] = None

    is_rated: bool = False

    created_at: datetime

    updated_at: Optional[
        datetime
    ] = None

    model_config = ConfigDict(
        from_attributes=True
    )


class TripRatingRequest(BaseModel):

    score: int

    comment: Optional[
        str
    ] = None


class TripLocationBase(BaseModel):

    trip_id: uuid.UUID

    lat: Optional[
        Decimal
    ] = None

    lng: Optional[
        Decimal
    ] = None


class TripLocationCreate(
    TripLocationBase
):
    pass


class TripLocationUpdate(BaseModel):

    lat: Optional[
        Decimal
    ] = None

    lng: Optional[
        Decimal
    ] = None

class TripLocationResponse(
    TripLocationBase
):

    id: uuid.UUID

    created_at: Optional[
        datetime
    ] = None

    model_config = ConfigDict(
        from_attributes=True
    )

class ParcelBase(BaseModel):

    trip_id: uuid.UUID

    sender_name: str

    sender_phone: str

    receiver_name: str

    receiver_phone: str

    receiver_address: str

    package_type: PackageType

    weight_kg: Optional[
        Decimal
    ] = None

    cod_amount: Decimal = Decimal(
        "0.00"
    )

    pod_photo_url: Optional[
        str
    ] = None

    pod_signature_url: Optional[
        str
    ] = None

    pod_otp: Optional[
        str
    ] = None

    status: str = "pending"


class ParcelCreate(ParcelBase):
    pass


class ParcelUpdate(BaseModel):

    sender_name: Optional[
        str
    ] = None

    sender_phone: Optional[
        str
    ] = None

    receiver_name: Optional[
        str
    ] = None

    receiver_phone: Optional[
        str
    ] = None

    receiver_address: Optional[
        str
    ] = None

    package_type: Optional[
        PackageType
    ] = None

    weight_kg: Optional[
        Decimal
    ] = None

    cod_amount: Optional[
        Decimal
    ] = None

    pod_photo_url: Optional[
        str
    ] = None

    pod_signature_url: Optional[
        str
    ] = None

    pod_otp: Optional[
        str
    ] = None

    status: Optional[
        str
    ] = None


class ParcelResponse(ParcelBase):

    id: uuid.UUID

    created_at: Optional[
        datetime
    ] = None

    updated_at: Optional[
        datetime
    ] = None

    model_config = ConfigDict(
        from_attributes=True
    )
