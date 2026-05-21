import uuid

from datetime import datetime
from decimal import Decimal

from typing import Optional, List

from pydantic import (
    BaseModel,
    ConfigDict
)

from app.core.enums import (
    ServiceType,
    TripStatus,
    PackageType
)

# =========================================================
# TRIP ESTIMATE SCHEMAS
# =========================================================

class TripEstimateRequest(BaseModel):

    vehicle_category: str

    distance_km: Decimal


class TripEstimateResponse(BaseModel):

    vehicle_category: str

    distance_km: Decimal

    estimated_fare: Decimal


# =========================================================
# TRIP SCHEMAS
# =========================================================

class TripBase(BaseModel):

    customer_id: uuid.UUID

    driver_id: Optional[
        uuid.UUID
    ] = None

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

    fare: Optional[
        Decimal
    ] = None


# =========================================================
# CREATE TRIP
# =========================================================

class TripCreate(TripBase):

    estimated_distance: Optional[
        Decimal
    ] = None

    estimated_fare: Optional[
        Decimal
    ] = None

    vehicle_category: Optional[
        str
    ] = None


# =========================================================
# UPDATE TRIP
# =========================================================

class TripUpdate(BaseModel):

    driver_id: Optional[
        uuid.UUID
    ] = None

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

    fare: Optional[
        Decimal
    ] = None


# =========================================================
# TRIP RESPONSE
# =========================================================

class TripResponse(TripBase):

    id: uuid.UUID

    status: TripStatus

    estimated_distance: Optional[
        Decimal
    ] = None

    estimated_fare: Optional[
        Decimal
    ] = None

    vehicle_category: Optional[
        str
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

    is_rated: bool = False

    created_at: datetime

    updated_at: Optional[
        datetime
    ] = None

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# TRIP RATING REQUEST
# =========================================================

class TripRatingRequest(BaseModel):

    stars: int

    feedback: Optional[
        str
    ] = None


# =========================================================
# TRIP LOCATION SCHEMAS
# =========================================================

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


# =========================================================
# PARCEL SCHEMAS
# =========================================================

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


# =========================================================
# CREATE PARCEL
# =========================================================

class ParcelCreate(ParcelBase):
    pass


# =========================================================
# UPDATE PARCEL
# =========================================================

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


# =========================================================
# PARCEL RESPONSE
# =========================================================

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